from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from context_manager import (
    get_context,
    generate_mcqs,
    feynman_explanation,
    compute_relevance_score,
)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Autonomous Learning Agent",
    page_icon="🧠",
    layout="centered"
)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
    <h1 style='text-align: center;'>🧠 Autonomous Learning Agent</h1>
    <p style='text-align: center; color: gray;'>
    Adaptive learning using checkpoints, 70% mastery rule, and Feynman technique
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Topic Input Card (UI only)
# -----------------------------
st.subheader("Select Topic to Learn")

# =============================
# UPDATED: light UI styling (avoid dark appearance)
# =============================
st.markdown(
    """
    <style>
      /* UPDATED: enforce light theme + readable colors everywhere */
      :root { color-scheme: light; }
      .stApp { background-color: #ffffff !important; color: #0f172a !important; }
      html, body, [class*="css"] { color: #0f172a !important; }
      [data-testid="stHeader"] { background: rgba(255,255,255,0.0); }
      .stMarkdown, .stMarkdown p, .stMarkdown li, .stCaption, .stAlert, label, .stRadio * {
        color: #0f172a !important;
      }
      .stTextInput input, .stTextArea textarea, .stSelectbox div, .stRadio div[role="radiogroup"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-color: #e2e8f0 !important;
      }
      /* Make radio option text readable */
      .stRadio label span { color: #0f172a !important; }
      /* Containers */
      [data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
      }
      /* UPDATED: make buttons look clean (not black) on light UI */
      .stButton > button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: 1px solid #1d4ed8 !important;
        border-radius: 10px !important;
        padding: 0.6rem 1rem !important;
        font-weight: 600 !important;
      }
      .stButton > button:hover {
        background-color: #1d4ed8 !important;
        border-color: #1e40af !important;
      }
      .stButton > button:disabled {
        background-color: #94a3b8 !important;
        border-color: #94a3b8 !important;
        color: #f8fafc !important;
      }
    </style>
    """,
    unsafe_allow_html=True
)

# =============================
# UPDATED UI: checkpoint-based selection + free search (mutually exclusive)
# =============================
CHECKPOINT_TOPICS = [
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "Computer Vision",
    "Reinforcement Learning",
    "Data Structures and Algorithms",
    "Cloud Computing",
    "Distributed Systems",
    "Cybersecurity Basics",
]
CHECKPOINT_PLACEHOLDER = "Please select a checkpoint topic"

# Track which input the user is actively using
if "active_source" not in st.session_state:
    st.session_state.active_source = None


def _on_checkpoint_change():
    # When user selects from checkpoint, clear search box
    st.session_state.active_source = "checkpoint"
    st.session_state.topic_input = ""


def _on_search_change():
    # When user types a search, reset checkpoint selection to placeholder
    st.session_state.active_source = "search"
    st.session_state.checkpoint_topic = CHECKPOINT_PLACEHOLDER


selected_checkpoint = st.selectbox(
    "Select Topic to Learn",
    [CHECKPOINT_PLACEHOLDER] + CHECKPOINT_TOPICS,
    index=0,
    key="checkpoint_topic",
    help="Predefined checkpoints for quick selection (Week 1-2 alignment).",
    on_change=_on_checkpoint_change,
)

st.subheader("🔎 Search or enter a topic")
topic_input = st.text_input(
    "Search or enter a topic",
    placeholder="e.g. Diffusion Models, Backpropagation, Transformers",
    key="topic_input",
    on_change=_on_search_change,
)

# Determine the final topic based on the active source (no conflicts)
final_topic = None
search_value = topic_input.strip()
checkpoint_value = selected_checkpoint

if st.session_state.get("active_source") == "search" and search_value:
    final_topic = search_value
elif st.session_state.get("active_source") == "checkpoint" and checkpoint_value != CHECKPOINT_PLACEHOLDER:
    final_topic = checkpoint_value
# Fallbacks if user hasn't interacted yet
elif search_value:
    final_topic = search_value
elif checkpoint_value != CHECKPOINT_PLACEHOLDER:
    final_topic = checkpoint_value

st.caption("Select a topic to start learning.")

if "stage" not in st.session_state:
    st.session_state.stage = "start"

if "score" not in st.session_state:
    st.session_state.score = None

# Track the active topic to keep the LangGraph-like flow deterministic
if "topic" not in st.session_state:
    st.session_state.topic = ""

# =============================
# UPDATED: state for MCQ evaluation
# =============================
if "explanation" not in st.session_state:
    st.session_state.explanation = ""
if "simple_explanation" not in st.session_state:
    st.session_state.simple_explanation = ""
if "mcqs" not in st.session_state:
    st.session_state.mcqs = []

if "mcq_answers" not in st.session_state:
    # stores selected option index for each question (0..3) or None
    st.session_state.mcq_answers = {}

if "relevance_score" not in st.session_state:
    st.session_state.relevance_score = None

# =============================
# UPDATED: quiz attempts (max 3 tries with re-explain + re-quiz)
# =============================
MAX_ATTEMPTS = 3
if "attempt" not in st.session_state:
    st.session_state.attempt = 1


# Helper: move to next checkpoint topic (UI only)
def _get_next_checkpoint_topic(current_topic: str):
    if current_topic in CHECKPOINT_TOPICS:
        idx = CHECKPOINT_TOPICS.index(current_topic)
        if idx + 1 < len(CHECKPOINT_TOPICS):
            return CHECKPOINT_TOPICS[idx + 1]
    return None


def _reset_for_new_topic(topic_value: str):
    """UI-only reset for starting or switching topics."""
    st.session_state.topic = topic_value
    st.session_state.stage = "teaching"
    st.session_state.relevance_score = None
    st.session_state.score = None
    st.session_state.explanation = ""
    st.session_state.simple_explanation = ""
    st.session_state.mcqs = []
    st.session_state.mcq_answers = {}
    st.session_state.attempt = 1

# =============================
# UPDATED UI: Start Learning always visible; guard with topic validation
# =============================
start_clicked = st.button("🚀 Start Learning", use_container_width=True)
if start_clicked:
    if final_topic:
        _reset_for_new_topic(final_topic)
        st.rerun()
    else:
        st.warning("Please select or search a topic first.")

# -----------------------------
# Teaching Stage
# -----------------------------
if st.session_state.stage == "teaching":
    st.divider()
    # =============================
    # UPDATED UI: Explanation in its own box
    # =============================
    with st.container(border=True):
        st.subheader("📘 Explanation")
        st.session_state.explanation = get_context(st.session_state.topic)
        st.write(st.session_state.explanation)
        st.caption("Step flow: topic → explain → quiz → score → Feynman.")

    # =============================
    # UPDATED: show "Start Quiz" button after explanation
    # =============================
    if st.button("📝 Start Quiz", use_container_width=True):
        st.session_state.attempt = 1
        st.session_state.score = None
        # =============================
        # UPDATED: MCQs derived ONLY from what was explained
        # =============================
        # Backward-compatible call (in case Streamlit server has an older function loaded)
        try:
            st.session_state.mcqs = generate_mcqs(
                st.session_state.topic,
                context_text=st.session_state.explanation,
                difficulty="normal",
            )
        except TypeError:
            # Fallback: generate without context constraint (requires server restart to pick up new signature)
            st.session_state.mcqs = generate_mcqs(st.session_state.topic)

        st.session_state.relevance_score = compute_relevance_score(
            st.session_state.explanation,
            st.session_state.mcqs,
        )
        st.session_state.mcq_answers = {i: None for i in range(len(st.session_state.mcqs))}
        st.session_state.stage = "quiz"
        st.rerun()

# -----------------------------
# Answer & Evaluation
# -----------------------------
if st.session_state.stage == "quiz":
    st.divider()
    # =============================
    # UPDATED UI: Explanation box (separate)
    # =============================
    with st.container(border=True):
        st.subheader("📘 Explanation")
        st.write(st.session_state.explanation or "Explanation not available.")

    mcqs = st.session_state.mcqs or []
    answers = st.session_state.mcq_answers or {}

    # =============================
    # UPDATED UI: Quiz box (separate)
    # =============================
    with st.container(border=True):
        st.subheader(f"❓ Quiz (10 MCQs) — Attempt {st.session_state.attempt}/{MAX_ATTEMPTS}")
        if st.session_state.relevance_score is not None:
            st.info(f"Question relevance: {st.session_state.relevance_score}%")

        # If quiz didn't load, regenerate and rerun (keeps UI consistent)
        if len(mcqs) != 10:
            st.warning("Quiz questions were not loaded. Regenerating quiz now...")
            try:
                st.session_state.mcqs = generate_mcqs(
                    st.session_state.topic,
                    context_text=st.session_state.explanation,
                    difficulty="normal" if st.session_state.attempt == 1 else "easy",
                )
            except TypeError:
                st.session_state.mcqs = generate_mcqs(st.session_state.topic)
            st.session_state.relevance_score = compute_relevance_score(
                st.session_state.explanation,
                st.session_state.mcqs,
            )
            st.session_state.mcq_answers = {i: None for i in range(len(st.session_state.mcqs))}
            st.rerun()

        for idx, q in enumerate(st.session_state.mcqs, start=1):
            st.markdown(f"**Q{idx}. {q['question']}**")
            choice = st.radio(
                label=f"Select an option for Q{idx}",
                options=list(range(4)),
                format_func=lambda i, opts=q["options"]: opts[i],
                index=answers.get(idx - 1, None),
                key=f"mcq_{idx}",
            )
            st.session_state.mcq_answers[idx - 1] = choice
            st.divider()

    answered_all = (len(st.session_state.mcqs) == 10) and all(
        st.session_state.mcq_answers.get(i) is not None for i in range(len(st.session_state.mcqs))
    )

    # =============================
    # UPDATED UI: Submit box (separate)
    # =============================
    with st.container(border=True):
        st.subheader("✅ Submit Answers")
        if st.button("✅ Submit MCQs", use_container_width=True):
            if not answered_all:
                st.warning("Please answer all 10 MCQs to get an accurate score.")
                st.stop()

            correct = 0
            for i, q in enumerate(st.session_state.mcqs):
                if st.session_state.mcq_answers.get(i) == q.get("answer_index"):
                    correct += 1
            st.session_state.score = int((correct / 10) * 100)
            st.session_state.stage = "result"
            st.rerun()

# -----------------------------
# Result + 70% rule + retry up to 3 times
# -----------------------------
if st.session_state.stage == "result":
    st.divider()
    score = st.session_state.score if st.session_state.score is not None else 0

    # =============================
    # UPDATED UI: Score & feedback box
    # =============================
    with st.container(border=True):
        st.subheader("📊 Score & Feedback")
        st.write(f"**Topic:** {st.session_state.topic}")
        st.write(f"**Score:** {score}%")

        if score >= 70:
            st.success("Congratulations! You understood the topic.")
        else:
            st.error("Below 70% mastery. Feynman re-teaching is triggered.")

    # Success path: Learn Next Topic button (auto-advance through checkpoints)
    if score >= 70:
        with st.container(border=True):
            st.subheader("➡️ Next Step")
            next_topic = _get_next_checkpoint_topic(st.session_state.topic)
            if next_topic:
                if st.button("Learn Next Topic", use_container_width=True):
                    # UI-only: set checkpoint selection to next and start teaching immediately
                    st.session_state.active_source = "checkpoint"
                    st.session_state.checkpoint_topic = next_topic
                    st.session_state.topic_input = ""
                    _reset_for_new_topic(next_topic)
                    st.rerun()
            else:
                st.info("You have completed all topics.")
                # Keep stage available for user to reselect any topic above
    else:
        # Failure path: Feynman box + retry
        with st.container(border=True):
            st.subheader("🔁 Feynman Re-Explanation")
            st.session_state.simple_explanation = feynman_explanation(st.session_state.topic)
            st.write(st.session_state.simple_explanation)

        if st.session_state.attempt < MAX_ATTEMPTS:
            if st.button("📝 Start Quiz Again", use_container_width=True):
                st.session_state.attempt += 1
                st.session_state.score = None
                try:
                    st.session_state.mcqs = generate_mcqs(
                        st.session_state.topic,
                        context_text=st.session_state.simple_explanation,
                        difficulty="easy",
                    )
                except TypeError:
                    st.session_state.mcqs = generate_mcqs(st.session_state.topic)
                st.session_state.relevance_score = compute_relevance_score(
                    st.session_state.simple_explanation,
                    st.session_state.mcqs,
                )
                st.session_state.mcq_answers = {i: None for i in range(len(st.session_state.mcqs))}
                st.session_state.stage = "quiz"
                st.rerun()
        else:
            with st.container(border=True):
                st.warning("Maximum attempts reached (3). Please review and try again.")
                if st.button("↩️ Back to Topic Selection", use_container_width=True):
                    st.session_state.stage = "start"
                    st.rerun()

# -----------------------------
# End Message
# -----------------------------
if st.session_state.stage == "done":
    st.divider()
    # =============================
    # UPDATED UI: reset box (re-learning without restarting app)
    # =============================
    with st.container(border=True):
        st.subheader("🔄 Reset / Re-learn")
        st.caption("You can select any topic above and click Start Learning again.")
        if st.button("Reset Current Session", use_container_width=True):
            st.session_state.stage = "start"
            st.session_state.score = None
            st.session_state.explanation = ""
            st.session_state.simple_explanation = ""
            st.session_state.relevance_score = None
            st.session_state.mcqs = []
            st.session_state.mcq_answers = {}
            st.session_state.attempt = 1
            st.session_state.topic = ""
            st.rerun()
