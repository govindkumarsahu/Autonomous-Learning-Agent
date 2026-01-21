from checkpoints import CHECKPOINTS
from context_manager import (
    get_context,
    generate_mcqs,
    feynman_explanation
)

print("\nAI Autonomous Learning Started\n")

for cp in CHECKPOINTS:
    print("Checkpoint:", cp["topic"])

    # Step 1: Explanation
    explanation = get_context(cp["topic"])
    print("\nAI Explanation:")
    print(explanation)

    # =============================
    # UPDATED: MCQ evaluation (10 questions, score out of 100)
    # =============================
    print("\nMCQ Evaluation (10 Questions):")
    mcqs = generate_mcqs(cp["topic"])
    correct = 0

    for i, q in enumerate(mcqs, start=1):
        print(f"\nQ{i}. {q['question']}")
        for opt_idx, opt_text in enumerate(q["options"]):
            print(f"  {opt_idx + 1}. {opt_text}")
        while True:
            try:
                choice = int(input("Your choice (1-4): ").strip())
                if choice in (1, 2, 3, 4):
                    break
            except Exception:
                pass
            print("Please enter a valid option (1-4).")

        if (choice - 1) == q["answer_index"]:
            correct += 1

    score = int((correct / 10) * 100)
    print(f"\nYour Score: {score}%")

    if score >= 70:
        print("✅ Passed! Moving to next checkpoint.")
    else:
        print("❌ Failed! Re-explaining using Feynman method.")
        simple_explanation = feynman_explanation(cp["topic"])
        print("\nFeynman Explanation:")
        print(simple_explanation)

    print("\n" + "-" * 50 + "\n")

print("🎉 Learning Session Completed")
