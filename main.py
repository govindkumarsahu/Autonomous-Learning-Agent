from checkpoints import CHECKPOINTS
from context_manager import (
    get_context,
    generate_questions,
    evaluate_answer,
    feynman_explanation
)

print("\nAI Autonomous Learning Started\n")

for cp in CHECKPOINTS:
    print("Checkpoint:", cp["topic"])

    # Step 1: Explanation
    explanation = get_context(cp["topic"])
    print("\nAI Explanation:")
    print(explanation)

    # Step 2: Questions
    print("\nAI Questions:")
    questions = generate_questions(cp["topic"])
    print(questions)

    # Step 3: User Answer
    user_answer = input("\nYour Answer: ")

    # Step 4: Evaluation (70% rule)
    score = evaluate_answer(user_answer, cp["topic"])
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
