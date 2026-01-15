import streamlit as st
from context_manager import (
    get_context,
    generate_questions,
    evaluate_answer,
    feynman_explanation
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
# Topic Input Card
# -----------------------------
st.subheader("📌 Learning Setup")

topic = st.text_input("Enter a topic to learn", placeholder="e.g. What is Agent?")

if "stage" not in st.session_state:
    st.session_state.stage = "start"

if "score" not in st.session_state:
    st.session_state.score = None

if st.button("🚀 Start Learning", use_container_width=True) and topic:
    st.session_state.stage = "teaching"

# -----------------------------
# Teaching Stage
# -----------------------------
if st.session_state.stage == "teaching":
    st.divider()
    st.subheader("📘 AI Explanation")

    with st.container(border=True):
        explanation = get_context(topic)
        st.write(explanation)

    st.subheader("❓ Questions")
    with st.container(border=True):
        questions = generate_questions(topic)
        st.write(questions)

    st.session_state.stage = "answer"

# -----------------------------
# Answer & Evaluation
# -----------------------------
if st.session_state.stage == "answer":
    st.divider()
    st.subheader("✍️ Your Answer")

    user_answer = st.text_area(
        "Write your answer below",
        height=150,
        placeholder="Explain in your own words..."
    )

    if st.button("✅ Submit Answer", use_container_width=True):
        score = evaluate_answer(user_answer, topic)
        st.session_state.score = score

        st.divider()

        if score >= 70:
            st.success(f"🎉 Passed! Score: {score}%")
            st.info("You have successfully understood the topic.")
            st.session_state.stage = "done"
        else:
            st.error(f"❌ Failed | Score: {score}%")

            st.subheader("🎓 Feynman Re-Explanation")
            with st.container(border=True):
                feynman_text = feynman_explanation(topic)
                st.write(feynman_text)

            st.session_state.stage = "done"

# -----------------------------
# End Message
# -----------------------------
if st.session_state.stage == "done":
    st.divider()
    st.caption("🔁 Refresh the page to try a new topic.")
