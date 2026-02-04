
from datetime import datetime, timedelta, timezone
from typing import List
import pytz

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

from auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from context_manager import ContextManager
from database import get_database
from models import Token, UserCreate


app = FastAPI(title="Autonomous Learning Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


context_manager = ContextManager()


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=2)


class ExplainResponse(BaseModel):
    explanation: str


class Question(BaseModel):
    question: str
    options: List[str] = Field(..., min_length=4, max_length=4)
    answer_index: int = Field(..., ge=0, le=3)


class GenerateQuizRequest(BaseModel):
    topic: str = Field(..., min_length=2)


class GenerateQuizResponse(BaseModel):
    questions: List[Question] = Field(..., min_length=10, max_length=10)
    relevance_score: int = Field(..., ge=0, le=100)


class EvaluateRequest(BaseModel):
    topic: str = Field(..., min_length=2)
    answers: List[int] = Field(..., min_length=10, max_length=10)
    correct_answers: List[int] = Field(..., min_length=10, max_length=10)


class EvaluateResponse(BaseModel):
    score: int = Field(..., ge=0, le=100)
    attempt_number: int
    max_attempts_reached: bool


class ReteachRequest(BaseModel):
    topic: str = Field(..., min_length=2)


class ReteachResponse(BaseModel):
    simplified_explanation: str


@app.get("/")
def health():
    return {
        "status": "ok",
        "llm_configured": context_manager.has_llm(),
    }


# ============ Authentication Endpoints ============


@app.post("/register")
async def register(user: UserCreate):
    db = get_database()
    
    # Check if user exists
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    hashed_password = get_password_hash(user.password)
    ist = pytz.timezone('Asia/Kolkata')
    user_dict = {
        "email": user.email,
        "hashed_password": hashed_password,
        "created_at": datetime.now(ist)
    }
    await db.users.insert_one(user_dict)
    
    return {"message": "User created successfully", "email": user.email}


@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_database()
    
    user = await db.users.find_one({"email": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return {"email": current_user["email"]}


@app.get("/progress")
async def get_progress(current_user: dict = Depends(get_current_user)):
    db = get_database()
    
    # Get all progress records for this user
    progress_records = await db.progress.find(
        {"user_id": str(current_user["_id"])}
    ).sort("date", -1).to_list(length=100)
    
    # Convert ObjectId to string for JSON serialization
    for record in progress_records:
        record["_id"] = str(record["_id"])
    
    return {"progress": progress_records}


# ============ Learning Endpoints (Protected) ============


@app.post("/explain", response_model=ExplainResponse)
async def explain(req: ExplainRequest, current_user: dict = Depends(get_current_user)):
    # Explanation is cached per topic in-memory to keep quizzes grounded.
    explanation = context_manager.explain(req.topic)
    return ExplainResponse(explanation=explanation)


@app.post("/generate-quiz", response_model=GenerateQuizResponse)
async def generate_quiz(req: GenerateQuizRequest, current_user: dict = Depends(get_current_user)):
    questions, _relevance = context_manager.generate_quiz(req.topic)

    if len(questions) != 10:
        # Business rule: always exactly 10 MCQs
        raise HTTPException(status_code=500, detail="Quiz generation did not produce exactly 10 questions")

    # Requirement: always return 100 (do not randomize).
    return GenerateQuizResponse(questions=questions, relevance_score=100)


@app.post("/evaluate", response_model=EvaluateResponse)
async def evaluate(req: EvaluateRequest, current_user: dict = Depends(get_current_user)):
    if len(req.answers) != len(req.correct_answers):
        raise HTTPException(status_code=400, detail="answers and correct_answers length mismatch")
    if len(req.answers) != 10:
        raise HTTPException(status_code=400, detail="Expected exactly 10 answers")

    correct = 0
    for user_ans, correct_ans in zip(req.answers, req.correct_answers):
        if not (0 <= user_ans <= 3) or not (0 <= correct_ans <= 3):
            raise HTTPException(status_code=400, detail="Answer indices must be between 0 and 3")
        if user_ans == correct_ans:
            correct += 1

    # Business rule: percentage score
    score = int((correct / 10) * 100)
    
    # Get database and check attempt count
    db = get_database()
    user_id = str(current_user["_id"])
    
    # Count existing attempts for this topic
    existing_attempts = await db.progress.count_documents({
        "user_id": user_id,
        "topic": req.topic
    })
    
    attempt_number = existing_attempts + 1
    
    # Check if max attempts reached
    if attempt_number > 3:
        raise HTTPException(
            status_code=400,
            detail="Maximum 3 attempts reached for this topic"
        )
    
    # Save progress to database
    ist = pytz.timezone('Asia/Kolkata')
    progress_record = {
        "user_id": user_id,
        "topic": req.topic,
        "attempt_number": attempt_number,
        "score": score,
        "date": datetime.now(ist)
    }
    await db.progress.insert_one(progress_record)
    
    max_attempts_reached = (attempt_number == 3 and score < 70)
    
    return EvaluateResponse(
        score=score,
        attempt_number=attempt_number,
        max_attempts_reached=max_attempts_reached
    )


@app.post("/reteach", response_model=ReteachResponse)
async def reteach(req: ReteachRequest, current_user: dict = Depends(get_current_user)):
    simplified = context_manager.reteach(req.topic)
    return ReteachResponse(simplified_explanation=simplified)

