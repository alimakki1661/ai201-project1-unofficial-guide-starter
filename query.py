"""
query.py — End-to-end query function for The Unofficial Guide
Milestone 5: retrieve → ground → generate → return answer + sources
"""

import os
from dotenv import load_dotenv
from groq import Groq
from retrieval import build_vector_store, retrieve, TOP_K

# Load GROQ_API_KEY from .env
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
LLM_MODEL = "llama-3.3-70b-versatile"

# System prompt — strictly enforces grounding
SYSTEM_PROMPT = """You are a helpful assistant answering questions about College of Staten Island Computer Science professors. You will be given a question and a set of student reviews retrieved from Rate My Professors.

CRITICAL RULES:
1. Answer ONLY using information from the provided reviews. Do NOT use any outside knowledge about these professors or any other topic.
2. If the reviews do not contain enough information to answer the question, respond exactly: "I don't have enough information in the documents to answer that."
3. Do not make up details, ratings, course codes, or facts that are not explicitly stated in the reviews.
4. When you reference an opinion or fact, you can mention it came from student reviews.
5. Be concise and direct. Do not pad your answer with unnecessary commentary."""


def ask(question: str, collection=None, model=None) -> dict:
    """
    Answer a question using grounded retrieval + LLM generation.
    
    Returns a dict with:
        - answer: the LLM's response (string)
        - sources: list of unique source filenames the answer drew from
        - retrieved_chunks: full list of retrieved chunks (for debugging/eval)
    """
    # If no vector store passed in, build one (slow — better to pass it in for repeated queries)
    if collection is None or model is None:
        collection, model = build_vector_store()
    
    # Retrieve top-k chunks
    retrieved = retrieve(collection, model, question, k=TOP_K)
    
    # Build the context block for the LLM
    context_lines = []
    for i, r in enumerate(retrieved, 1):
        context_lines.append(f"[Document {i} — source: {r['source']}]")
        context_lines.append(r['text'])
        context_lines.append("")  # blank line between docs
    context = "\n".join(context_lines)
    
    # Build the user message
    user_message = f"""Question: {question}

Retrieved student reviews:
{context}

Answer the question using only the information in the reviews above. If the reviews do not contain enough information, say so."""
    
    # Call the LLM
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,  # low temperature for more grounded/factual answers
    )
    
    answer = response.choices[0].message.content
    
    # Collect unique source filenames used
    sources = sorted(set(r['source'] for r in retrieved))
   
    
    return {
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": retrieved,
    }


if __name__ == "__main__":
    print("Building vector store (one-time setup)...")
    collection, model = build_vector_store()
    
    # Test with 2-3 of your evaluation questions
    test_questions = [
        "Is attendance mandatory in Professor Jahaj's CSC220 course?",
        "How does Professor Edemacu structure his CSC326 course?",
        "What is Professor Petingi's research area?",  # out-of-scope test
    ]
    
    for q in test_questions:
        print(f"\n{'=' * 70}")
        print(f"Q: {q}")
        print(f"{'=' * 70}")
        result = ask(q, collection, model)
        print(f"\nA: {result['answer']}")
        print(f"\nSources used:")
        for src in result['sources']:
            print(f"  • {src}")