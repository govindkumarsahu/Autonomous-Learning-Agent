from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables
# Try loading from .env file in current directory
env_loaded = load_dotenv()

# Also try loading from parent directory (in case VS Code runs from subdirectory)
if not env_loaded:
    env_loaded = load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Get API key - prefer GOOGLE_API_KEY, fallback to GEMINI_API_KEY
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

# Validate API key
if not api_key:
    env_file_path = os.path.join(os.path.dirname(__file__), '.env')
    raise ValueError(
        f"API key not found!\n"
        f"Please set either GOOGLE_API_KEY or GEMINI_API_KEY in:\n"
        f"1. Your .env file at: {env_file_path}\n"
        f"2. Or as environment variables\n\n"
        f"VS Code Tip: Make sure:\n"
        f"- .env file exists in the project root\n"
        f"- VS Code is using the virtual environment (venv)\n"
        f"- Python extension is configured to load .env file"
    )

# Initialize Gemini LLM
# Using gemini-2.5-flash which is available and fast
# Other available models: gemini-2.5-pro, gemini-pro-latest, gemini-flash-latest
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.3,
    google_api_key=api_key
)

def get_context(topic):
    try:
        prompt = (
            f"Explain the topic '{topic}' in very simple English. "
            f"Use short sentences and easy words."
        )
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg or "authentication" in error_msg.lower():
            raise ValueError(
                f"API authentication failed: {error_msg}\n"
                "Please check your GOOGLE_API_KEY or GEMINI_API_KEY in the .env file."
            ) from e
        if "NOT_FOUND" in error_msg or "not found" in error_msg.lower():
            raise ValueError(
                f"Model not found: {error_msg}\n"
                "Try changing the model name in context_manager.py to one of: "
                "gemini-2.5-flash, gemini-2.5-pro, gemini-pro-latest, or gemini-flash-latest"
            ) from e
        raise


def generate_questions(topic):
    try:
        prompt = (
            f"Generate 3 very simple questions on the topic '{topic}'. "
            f"Questions should be easy for beginners."
        )
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg or "authentication" in error_msg.lower():
            print(f"Warning: API authentication failed: {error_msg}")
            print("Falling back to default questions.")
        return (
            "1. What does this topic mean?\n"
            "2. Why is this topic important?\n"
            "3. Give one simple example."
        )


def evaluate_answer(user_answer, topic):
    try:
        prompt = f"""
        Topic: {topic}

        User Answer:
        {user_answer}

        Give a score out of 100 based on correctness.
        Only return the number.
        """
        response = llm.invoke(prompt)
        score = int("".join(filter(str.isdigit, response.content)))
        return score
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg or "authentication" in error_msg.lower():
            print(f"Warning: API authentication failed: {error_msg}")
            print("Falling back to default scoring.")
        if len(user_answer.strip()) > 20:
            return 75
        else:
            return 40


def feynman_explanation(topic):
    try:
        prompt = (
            f"Explain '{topic}' like teaching a 10-year-old. "
            f"Use very simple words and a real-life example."
        )
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg or "authentication" in error_msg.lower():
            print(f"Warning: API authentication failed: {error_msg}")
            print("Falling back to default explanation.")
        return (
            f"{topic} means making machines smart. "
            "Just like humans learn from experience, machines also learn from data."
        )
