"""
evaluate.py — Run all 5 evaluation questions and save results
Milestone 6: evaluation report
"""

from query import ask
from retrieval import build_vector_store

# Your 5 evaluation questions from planning.md, with their expected answers
EVAL_QUESTIONS = [
    {
        "id": "Q1",
        "question": "Is attendance mandatory in Professor Jahaj's CSC220 course?",
        "expected": "No. Multiple reviews state that attendance is not mandatory.",
    },
    {
        "id": "Q2",
        "question": "How does Professor Edemacu structure his CSC326 course?",
        "expected": "He gives two quizzes and a group project before the final. The final is open-book with notes allowed.",
    },
    {
        "id": "Q3",
        "question": "How do students feel about Professor Rao?",
        "expected": "Most reviews are negative. He has a 1.9/5 overall rating with 15 of 24 ratings being 1-star. Frequent complaints include communication, condescension, and excessive testing.",
    },
    {
        "id": "Q4",
        "question": "Which professors teach CSC326 at CSI?",
        "expected": "Edemacu Kennedy and Tatiana Anderson.",
    },
    {
        "id": "Q5",
        "question": "What is Professor Petingi's research area?",
        "expected": "The system should say it doesn't have enough information. The reviews focus on his teaching of CSC382 and don't discuss his research.",
    },
]


def main():
    print("Building vector store...")
    collection, model = build_vector_store()
    print()
    
    # Save full output to a file
    with open("evaluation_results.md", "w", encoding="utf-8") as f:
        f.write("# Evaluation Results\n\n")
        
        for item in EVAL_QUESTIONS:
            f.write(f"## {item['id']}: {item['question']}\n\n")
            f.write(f"**Expected answer:** {item['expected']}\n\n")
            
            result = ask(item["question"], collection, model)
            
            f.write(f"**System response:**\n\n{result['answer']}\n\n")
            f.write(f"**Sources retrieved:**\n")
            for src in result["sources"]:
                f.write(f"- {src}\n")
            f.write("\n")
            
            f.write(f"**Top retrieved chunks (with distance):**\n\n")
            for rank, chunk in enumerate(result["retrieved_chunks"], 1):
                preview = chunk["text"][:250].replace("\n", " ")
                f.write(f"{rank}. `{chunk['source']}` (distance: {chunk['distance']:.3f}): {preview}...\n")
            f.write("\n")
            
            f.write(f"**Accuracy judgment:** _TBD — fill in after reviewing_\n\n")
            f.write("---\n\n")
            
            # Also print to console as we go
            print(f"=== {item['id']}: {item['question']} ===")
            print(f"Answer: {result['answer'][:200]}...")
            print(f"Sources: {result['sources']}")
            print()
    
    print("Done! Full results saved to evaluation_results.md")


if __name__ == "__main__":
    main()