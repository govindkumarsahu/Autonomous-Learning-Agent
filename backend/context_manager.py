
import json
import os
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv

try:
    from langchain_groq import ChatGroq
except ModuleNotFoundError:
    ChatGroq = None


env_loaded = load_dotenv()
if not env_loaded:
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))


def _extract_json_object(text: str) -> Optional[str]:
    if not text:
        return None
    text = text.strip()
    if (text.startswith("{") and text.endswith("}")) or (text.startswith("[") and text.endswith("]")):
        return text
    match = re.search(r"(\{[\s\S]*\}|\[[\s\S]*\])", text)
    return match.group(1).strip() if match else None


def _safe_json_load(text: Optional[str]) -> Optional[Any]:
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def _medium_fallback_explanation(topic: str) -> str:
    return (
        f"## {topic}\n\n"
        "**Definition**\n"
        f"- {topic} is a concept/technology used in computer science and engineering.\n\n"
        "**Core Ideas**\n"
        "- What it is and what problem it solves\n"
        "- Key components/terms\n"
        "- How it works at a high level\n\n"
        "**Practical Examples**\n"
        "- Example 1: how it appears in real systems\n"
        "- Example 2: what engineers optimize or trade off\n\n"
        "**Key Takeaways**\n"
        f"- If you can define {topic}, describe the workflow, and give 1 real example, you understand the basics.\n"
    )


def _very_simple_fallback_explanation(topic: str) -> str:
    return (
        f"## {topic} (Feynman Style)\n\n"
        f"- {topic} is a technical idea used to solve a specific problem.\n"
        "- Think: input → processing → output.\n"
        "- If you can say what the input is, what happens in the middle, and what output you get, you understand it.\n"
    )


def _tokenize(text: str) -> set:
    return {w for w in re.findall(r"[A-Za-z0-9]+", (text or "").lower()) if len(w) > 3}


@dataclass
class ContextManager:
    """Stores per-topic generated content so downstream steps are grounded."""

    model: str = field(default_factory=lambda: os.getenv("GROQ_MODEL") or "llama-3.1-8b-instant")
    temperature: float = 0.3
    _llm: Any = field(init=False, default=None)
    _explanations: Dict[str, str] = field(init=False, default_factory=dict)
    _simplified: Dict[str, str] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")
        if api_key and ChatGroq is not None:
            self._llm = ChatGroq(model=self.model, temperature=self.temperature, groq_api_key=api_key)

    def has_llm(self) -> bool:
        return self._llm is not None

    def explain(self, topic: str, *, force: bool = False) -> str:
        if not force and topic in self._explanations:
            return self._explanations[topic]

        if self._llm is None:
            explanation = (
                "AI is not configured (missing GROQ_API_KEY or langchain-groq). Showing fallback explanation:\n\n"
                + _medium_fallback_explanation(topic)
            )
            self._explanations[topic] = explanation
            return explanation

        prompt = f"""
You are a senior engineering instructor. Explain the topic: "{topic}".

Requirements (B.Tech level, production-ready clarity):
- Audience: engineering students.
- Tone: professional, precise, and concise.
- Structure with short sections: definition, core concepts, math/notation (if relevant),
  typical workflow/architecture, constraints/performance trade-offs, common pitfalls,
  and 2 practical engineering examples.
- Add 3–5 key takeaways as bullet points.
- Keep it focused (~200–350 words).
"""
        response = self._llm.invoke(prompt)
        explanation = (response.content or "").strip() or _medium_fallback_explanation(topic)
        self._explanations[topic] = explanation
        return explanation

    def reteach(self, topic: str, *, force: bool = False) -> str:
        if not force and topic in self._simplified:
            return self._simplified[topic]

        if self._llm is None:
            simple = (
                "AI is not configured (missing GROQ_API_KEY or langchain-groq). Showing fallback reteach:\n\n"
                + _very_simple_fallback_explanation(topic)
            )
            self._simplified[topic] = simple
            return simple

        prompt = f"""
Re-teach the topic "{topic}" in a VERY SIMPLE way (Feynman style) without losing technical correctness.

Rules:
- Start with a 1–2 line intuition.
- Then explain the core idea in 5–10 bullet points.
- Include 2 engineering/CS examples.
- End with 3 short self-check questions.
"""
        response = self._llm.invoke(prompt)
        simple = (response.content or "").strip() or _very_simple_fallback_explanation(topic)
        self._simplified[topic] = simple
        return simple

    def _fallback_mcqs(self, topic: str, explanation: str) -> List[Dict[str, Any]]:
        basis_hint = (explanation or "").strip()[:160]
        base: List[Dict[str, Any]] = [
            {
                "question": f"Based on the explanation: {basis_hint}...\nWhich statement best matches the definition for '{topic}'?",
                "options": [
                    "A precise formal definition used in engineering",
                    "A purely opinion-based description",
                    "A historical anecdote unrelated to engineering practice",
                    "A marketing slogan without technical meaning",
                ],
                "answer_index": 0,
            },
            {
                "question": f"Based on the explanation: {basis_hint}...\nWhich option best represents a core idea mentioned?",
                "options": [
                    "A well-defined model/abstraction",
                    "Astrology-based assumptions",
                    "Random trial without evaluation",
                    "Undefined terms with no constraints",
                ],
                "answer_index": 0,
            },
        ]
        while len(base) < 10:
            i = len(base) + 1
            base.append(
                {
                    "question": f"Based on the explanation: {basis_hint}...\n[Demo] Which option is consistent with what was explained? (Q{i})",
                    "options": [
                        "Write a small example and test edge cases",
                        "Memorize without applying",
                        "Avoid definitions and rely only on intuition",
                        "Skip evaluation entirely",
                    ],
                    "answer_index": 0,
                }
            )
        return base[:10]

    def generate_quiz(self, topic: str) -> Tuple[List[Dict[str, Any]], int]:
        explanation = self._explanations.get(topic)
        if not explanation:
            explanation = self.explain(topic)

        if self._llm is None:
            mcqs = self._fallback_mcqs(topic, explanation)
            return mcqs, self.compute_relevance_score(explanation, mcqs)

        prompt = f"""
You MUST generate MCQs ONLY from the explanation text provided below. Do NOT use outside facts.

Topic: "{topic}"

Explanation text (the ONLY source):
<BEGIN_EXPLANATION>
{explanation}
<END_EXPLANATION>

Task: Generate EXACTLY 10 multiple-choice questions (MCQs) derived ONLY from the explanation text.

Rules:
- Exactly 10 questions.
- Each question MUST have exactly 4 options.
- Only ONE option is correct.
- Keep questions medium difficulty (engineering undergrad).
- Avoid ambiguous wording.
- Do not ask anything not explicitly stated or clearly implied in the explanation.

Return STRICT JSON ONLY (no markdown, no extra text) in this schema:
{{
  "questions": [
    {{
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "answer_index": 0
    }}
  ]
}}
"""
        response = self._llm.invoke(prompt)
        raw = (response.content or "").strip()
        data = _safe_json_load(_extract_json_object(raw))
        questions = (data or {}).get("questions") if isinstance(data, dict) else None
        if not isinstance(questions, list) or len(questions) != 10:
            mcqs = self._fallback_mcqs(topic, explanation)
            return mcqs, self.compute_relevance_score(explanation, mcqs)

        cleaned: List[Dict[str, Any]] = []
        for item in questions:
            if not isinstance(item, dict):
                continue
            q = str(item.get("question", "")).strip()
            opts = item.get("options", [])
            ans = item.get("answer_index", None)
            if not q or not isinstance(opts, list) or len(opts) != 4:
                continue
            try:
                ans_i = int(ans)
            except Exception:
                continue
            if ans_i < 0 or ans_i > 3:
                continue
            cleaned.append({"question": q, "options": [str(o).strip() for o in opts], "answer_index": ans_i})

        if len(cleaned) != 10:
            mcqs = self._fallback_mcqs(topic, explanation)
            return mcqs, self.compute_relevance_score(explanation, mcqs)

        return cleaned, self.compute_relevance_score(explanation, cleaned)

    def compute_relevance_score(self, explanation: str, questions: List[Dict[str, Any]]) -> int:
        if not explanation or not questions:
            return 0

        if self._llm is not None:
            try:
                formatted = "\n".join(
                    [
                        f"Q{i+1}: {q.get('question','')}\nOptions: {q.get('options', [])}"
                        for i, q in enumerate(questions[:10])
                    ]
                )
                prompt = f"""
Evaluate how well these MCQs are grounded ONLY in the provided explanation.
Return one integer 0-100 representing the percentage of questions that can be
answered directly from the explanation text.

Explanation:
<BEGIN_EXPLANATION>
{explanation}
<END_EXPLANATION>

MCQs:
{formatted}

Return only the integer percentage (no words).
"""
                response = self._llm.invoke(prompt)
                digits = "".join(filter(str.isdigit, (response.content or "")))
                if digits:
                    return max(0, min(100, int(digits)))
            except Exception:
                pass

        exp_tokens = _tokenize(explanation)
        if not exp_tokens:
            return 50

        overlaps: List[float] = []
        for q in questions:
            mcq_text = (q.get("question", "") or "") + " " + " ".join(q.get("options", []) or [])
            mcq_tokens = _tokenize(mcq_text)
            if not mcq_tokens:
                continue
            overlaps.append(len(mcq_tokens & exp_tokens) / max(1, len(mcq_tokens)))

        if not overlaps:
            return 50

        avg = sum(overlaps) / len(overlaps)
        return max(0, min(100, int((0.35 + avg) * 100)))

