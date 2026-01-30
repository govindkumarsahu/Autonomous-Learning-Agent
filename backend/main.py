
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .context_manager import ContextManager


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


@app.post("/explain", response_model=ExplainResponse)
def explain(req: ExplainRequest):
    # Explanation is cached per topic in-memory to keep quizzes grounded.
    explanation = context_manager.explain(req.topic)
    return ExplainResponse(explanation=explanation)


@app.post("/generate-quiz", response_model=GenerateQuizResponse)
def generate_quiz(req: GenerateQuizRequest):
    questions, _relevance = context_manager.generate_quiz(req.topic)

    if len(questions) != 10:
        # Business rule: always exactly 10 MCQs
        raise HTTPException(status_code=500, detail="Quiz generation did not produce exactly 10 questions")

    # Requirement: always return 100 (do not randomize).
    return GenerateQuizResponse(questions=questions, relevance_score=100)


@app.post("/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest):
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
    return EvaluateResponse(score=score)


@app.post("/reteach", response_model=ReteachResponse)
def reteach(req: ReteachRequest):
    simplified = context_manager.reteach(req.topic)
    return ReteachResponse(simplified_explanation=simplified)

