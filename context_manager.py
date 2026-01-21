"""
context_manager.py

Core LLM helpers for the Autonomous Learning Agent.
- Groq-backed LLM (LLama/Mixtral) with env-based key loading
- Explanation generation (professional, B.Tech level)
- MCQ generation (10 per topic, 4 options, single correct)
- Relevance scoring between explanation and MCQs
- Feynman-style re-teaching

LangGraph-style note:
- The Streamlit app uses explicit stage/state transitions (teach -> quiz -> score -> feynman)
  mirroring LangGraph node-by-node execution.
- LangSmith tracing can be enabled by setting LANGSMITH_* env vars and wiring callbacks
  into LangChain runnables (kept minimal here for demo safety).
"""

import json
import os
import re
from dotenv import load_dotenv

# =============================
# Groq client (safe import)
# =============================
try:
    from langchain_groq import ChatGroq
except ModuleNotFoundError:
    ChatGroq = None

# Load env from local .env (project root preferred)
env_loaded = load_dotenv()
if not env_loaded:
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Groq credentials + default model
api_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_MODEL") or "llama-3.1-8b-instant"

# =============================
# LLM init with safe fallback
# =============================
llm = None
if api_key and ChatGroq is not None:
    llm = ChatGroq(
        model=groq_model,
        temperature=0.3,
        groq_api_key=api_key,
    )
# LangSmith hint: set LANGSMITH_* env vars + callbacks to trace LangChain runs.


# =============================
# Fallback explanations (for offline/demo)
# =============================
def _medium_fallback_explanation(topic: str) -> str:
    return (
        f"## {topic} (Medium Explanation)\n\n"
        "**Definition**\n"
        f"- {topic} is a concept/technology used in computer science and engineering.\n\n"
        "**Core Ideas (what you should know)**\n"
        "- What it is and what problem it solves\n"
        "- Key components/terms (inputs, outputs, constraints)\n"
        "- How it works at a high level (steps or pipeline)\n\n"
        "**Engineering/CS Examples**\n"
        "- Example 1: Where this appears in software systems (e.g., web apps, databases, networking)\n"
        "- Example 2: How engineers use it in practice (e.g., performance, security, automation)\n\n"
        "**Common Mistakes**\n"
        "- Confusing definition with implementation details\n"
        "- Ignoring constraints (time/space/accuracy/security)\n\n"
        "**Quick Summary**\n"
        f"- If you can define {topic}, explain the main steps, and give 1 real example, you understand the basics.\n"
    )


def _very_simple_fallback_explanation(topic: str) -> str:
    return (
        f"## {topic} (Very Simple Explanation)\n\n"
        f"- {topic} is a technical idea used to solve a specific problem.\n"
        "- Think: input → processing → output.\n"
        "- If you can say what the input is, what happens in the middle, and what output you get, you understand it.\n"
    )


# =============================
# JSON helpers
# =============================
def _extract_json_object(text: str):
    """Extract the first JSON object/array from a string."""
    if not text:
        return None
    text = text.strip()
    if (text.startswith("{") and text.endswith("}")) or (text.startswith("[") and text.endswith("]")):
        return text
    match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
    return match.group(1).strip() if match else None


def _safe_json_load(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None


# =============================
# Professional explanation (B.Tech level)
# =============================
def get_context(topic: str) -> str:
    try:
        if llm is None:
            return (
                f"API is not configured, so I can't generate an AI explanation right now.\n\n"
                f"Topic: {topic}\n"
                "Fix:\n"
                "- Add `GROQ_API_KEY` in a `.env` file\n"
                "- Install dependency: `pip install langchain-groq groq`\n"
                "- Restart: `streamlit run app.py`"
            )

        prompt = f"""
You are a senior engineering instructor. Explain the topic: "{topic}".

Requirements (B.Tech level, production-ready clarity):
- Audience: B.Tech / technical degree students.
- Tone: professional, precise, and concise (avoid school-level simplification).
- Structure with short sections: definition, core concepts, math/notation (if relevant),
  typical workflow/architecture or pipeline, constraints/performance trade-offs,
  common misconceptions/pitfalls, and 2 practical engineering/CS examples.
- Add 3–5 key takeaways as bullet points the learner must retain.
- Keep it presentation-friendly and focused (about 200–350 words).
"""
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg or "authentication" in error_msg.lower():
            raise ValueError(
                f"API authentication failed: {error_msg}\n"
                "Please check your GROQ_API_KEY in the .env file."
            ) from e
        if "NOT_FOUND" in error_msg or "not found" in error_msg.lower():
            raise ValueError(
                f"Model not found: {error_msg}\n"
                "Try changing the Groq model name in context_manager.py to one of the available Groq models."
            ) from e
        if "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg:
            return (
                "AI service rate-limited (429). Showing fallback explanation:\n\n"
                + _medium_fallback_explanation(topic)
            )
        return (
            "AI service error occurred. Showing fallback explanation:\n\n"
            + _medium_fallback_explanation(topic)
        )


# =============================
# MCQ generation (10 Qs, 4 options, 1 correct)
# =============================
def generate_mcqs(topic, context_text=None, difficulty="normal"):
    """
    Returns a list of 10 MCQs.
    Each MCQ dict:
      {
        "question": str,
        "options": ["A ...", "B ...", "C ...", "D ..."],
        "answer_index": int,  # 0..3
        "explanation": str,
      }
    """
    # Fallback (API missing/unavailable): still return a demo-ready MCQ set.
    def _fallback():
        basis = (context_text or "").strip()
        basis_hint = f"Based on the provided explanation: {basis[:160]}..." if basis else "Based on the provided explanation."
        base = [
            {
                "question": f"{basis_hint}\nWhich statement best matches the definition stated for '{topic}'?",
                "options": [
                    "A precise formal definition used in engineering literature",
                    "A purely opinion-based description with no measurable criteria",
                    "A historical anecdote unrelated to engineering practice",
                    "A marketing slogan without technical meaning",
                ],
                "answer_index": 0,
                "explanation": "Technical topics are typically defined in formal, measurable terms.",
            },
            {
                "question": f"{basis_hint}\nWhich option best represents a core concept mentioned in the explanation?",
                "options": [
                    "A well-defined model/abstraction",
                    "Astrology-based assumptions",
                    "Random trial without evaluation",
                    "Undefined terminology with no constraints",
                ],
                "answer_index": 0,
                "explanation": "Engineering learning emphasizes abstractions, models, and constraints.",
            },
        ]
        while len(base) < 10:
            i = len(base) + 1
            base.append(
                {
                    "question": f"{basis_hint}\n[Demo] Which option is consistent with what was explained? (Q{i})",
                    "options": [
                        "Write a small example and test edge cases",
                        "Memorize a paragraph without applying it",
                        "Avoid definitions and rely only on intuition",
                        "Skip evaluation entirely",
                    ],
                    "answer_index": 0,
                    "explanation": "Applying concepts in small experiments and testing is a standard validation approach.",
                }
            )
        return base[:10]

    try:
        if llm is None:
            return _fallback()

        explanation_basis = (context_text or "").strip()
        if not explanation_basis:
            return _fallback()
        difficulty_line = (
            "Keep questions medium difficulty (B.Tech level)."
            if difficulty == "normal"
            else "Keep questions EASY and direct (based only on the explanation)."
        )

        prompt = f"""
You MUST generate MCQs ONLY from the explanation text provided below. Do NOT use outside facts.

Topic: "{topic}"

Explanation text (the ONLY source):
\"\"\"{explanation_basis}\"\"\"

Task: Generate EXACTLY 10 multiple-choice questions (MCQs) derived ONLY from the explanation text.

Rules:
- Exactly 10 questions.
- Each question MUST have exactly 4 options.
- Only ONE option is correct.
- {difficulty_line}
- Avoid ambiguous wording.
- Do not ask anything that is not explicitly stated or clearly implied in the explanation text.
- Keep terminology consistent with the explanation to maximize relevance/traceability.

Return STRICT JSON ONLY (no markdown, no extra text) in this schema:
{{
  "mcqs": [
    {{
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "answer_index": 0,
      "explanation": "string"
    }}
  ]
}}
"""
        response = llm.invoke(prompt)
        raw = response.content.strip()
        json_blob = _extract_json_object(raw)
        data = _safe_json_load(json_blob) if json_blob else None

        mcqs = (data or {}).get("mcqs") if isinstance(data, dict) else None
        if not isinstance(mcqs, list):
            return _fallback()

        cleaned = []
        for item in mcqs:
            if not isinstance(item, dict):
                continue
            q = str(item.get("question", "")).strip()
            opts = item.get("options", [])
            ans = item.get("answer_index", None)
            exp = str(item.get("explanation", "")).strip()
            if not q or not isinstance(opts, list) or len(opts) != 4:
                continue
            try:
                ans_i = int(ans)
            except Exception:
                continue
            if ans_i < 0 or ans_i > 3:
                continue
            cleaned.append(
                {
                    "question": q,
                    "options": [str(o).strip() for o in opts],
                    "answer_index": ans_i,
                    "explanation": exp,
                }
            )

        if len(cleaned) != 10:
            return _fallback()
        return cleaned

    except Exception as e:
        print(f"Warning: MCQ generation failed: {e}")
        return _fallback()


# =============================
# NEW: relevance scoring for MCQs vs explanation
# =============================
def compute_relevance_score(explanation: str, mcqs) -> int:
    """
    Estimate how well MCQs stay grounded in the provided explanation.
    Returns an integer percentage (0-100). Uses LLM rating when available,
    otherwise falls back to a simple lexical overlap heuristic.
    """
    if not explanation or not mcqs:
        return 0

    # Prefer LLM-based judgment
    if llm is not None:
        try:
            formatted_mcqs = "\n".join(
                [
                    f"Q{i+1}: {q.get('question','')}\nOptions: {q.get('options', [])}"
                    for i, q in enumerate(mcqs[:10])
                ]
            )
            prompt = f"""
Evaluate how well these MCQs are grounded ONLY in the provided explanation.
Return one integer 0-100 representing the percentage of questions that can be
answered directly from the explanation text.

Explanation:
\"\"\"{explanation}\"\"\"

MCQs:
{formatted_mcqs}

Return only the integer percentage (no words).
"""
            response = llm.invoke(prompt)
            digits = "".join(filter(str.isdigit, response.content))
            if digits:
                score = int(digits)
                return max(0, min(100, score))
        except Exception as exc:
            print(f"Warning: relevance scoring via LLM failed: {exc}")

    # Lexical overlap fallback
    def _tokenize(text):
        return {w for w in re.findall(r"[A-Za-z0-9]+", text.lower()) if len(w) > 3}

    explanation_tokens = _tokenize(explanation)
    if not explanation_tokens:
        return 50

    overlaps = []
    for q in mcqs:
        question_text = q.get("question", "")
        opts = " ".join(q.get("options", []))
        mcq_tokens = _tokenize(question_text + " " + opts)
        if not mcq_tokens:
            continue
        overlap = len(mcq_tokens & explanation_tokens) / max(1, len(mcq_tokens))
        overlaps.append(overlap)

    if not overlaps:
        return 50

    avg_overlap = sum(overlaps) / len(overlaps)
    return max(0, min(100, int((0.35 + avg_overlap) * 100)))


# =============================
# Text answer scoring (legacy, kept for completeness)
# =============================
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


# =============================
# Feynman re-teaching
# =============================
def feynman_explanation(topic):
    try:
        if llm is None:
            return (
                f"API is not configured, so I can't generate a Feynman re-explanation right now.\n\n"
                f"Topic: {topic}\n"
                "Add `GROQ_API_KEY` in a `.env` file and restart the app."
            )

        prompt = f"""
Re-teach the topic "{topic}" in a VERY SIMPLE way (Feynman style) without losing technical correctness.

Rules:
- Use short sentences and simple words.
- Start with a 1–2 line intuition.
- Then explain the core idea in 5–10 bullet points.
- Include 2 engineering/CS examples (e.g., networking, OS, databases, software architecture).
- End with 3 short self-check questions the student should be able to answer.
"""
        response = llm.invoke(prompt)
        return response.content.strip()
    except Exception as e:
        error_msg = str(e)
        if "API key" in error_msg or "authentication" in error_msg.lower():
            print(f"Warning: API authentication failed: {error_msg}")
            print("Falling back to default explanation.")
        return _very_simple_fallback_explanation(topic)
