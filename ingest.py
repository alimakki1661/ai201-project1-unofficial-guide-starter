"""
ingest.py — Document ingestion pipeline for The Unofficial Guide
Milestone 3: load → clean → chunk → inspect
"""

import re
import random
from pathlib import Path

DOCUMENTS_DIR = Path("documents")


def load_documents(docs_dir: Path) -> dict[str, str]:
    """Load all .txt files from the documents folder."""
    documents = {}
    for file_path in sorted(docs_dir.glob("*.txt")):
        with open(file_path, "r", encoding="utf-8") as f:
            documents[file_path.name] = f.read()
    return documents


def clean_document(raw_text: str) -> str:
    """
    Strip RMP boilerplate while keeping review content and rating data.
    
    Removes:
      - UI labels (Rate, Arrow Icon, Compare, I'm Professor X)
      - "AD" markers and ad placeholders
      - "Similar Professors" block (header + 5 names + 5 ratings = 7 lines)
      - "N Student Ratings" count header
      - "Helpful / Thumbs up / 0 / Thumbs down / 0" footer after each review
      - "All courses" / "Load More Ratings" filler
      - "Computer Icon" prefix on course codes
    
    Keeps:
      - Overall rating, % would take again, level of difficulty
      - Rating distribution counts (Awesome 5: 18, etc.)
      - Per-review metadata (Quality, Difficulty, course code, date, grade)
      - Review text and meaningful tags
    """
    lines = raw_text.split("\n")
    cleaned_lines = []
    i = 0
    
    junk_exact = {"AD", "Arrow Icon", "Compare", "All courses", "Load More Ratings"}
    
    while i < len(lines):
        line = lines[i].strip()
        
        if line in junk_exact:
            i += 1
            continue
        
        if line.startswith("I'm Professor "):
            i += 1
            continue
        
        if line == "Rate":
            i += 1
            continue
        
        # Skip "Similar Professors" block: header + 5 names + 5 ratings = 7 lines
        if line == "Similar Professors":
            i += 7
            continue
        
        # Skip "N Student Ratings" count header (redundant with header data)
        if re.match(r"^\d+ Student Ratings?$", line):
            i += 1
            continue
        
        # Skip "Helpful / Thumbs up / N / Thumbs down / N" pattern (5 lines)
        if line == "Helpful" and i + 1 < len(lines) and lines[i + 1].strip() == "Thumbs up":
            i += 5
            continue
        
        # Skip standalone "Thumbs up / N / Thumbs down / N" pattern (4 lines)
        if line == "Thumbs up":
            i += 4
            continue
        
        line = line.replace("Computer Icon", "")
        
        cleaned_lines.append(line)
        i += 1
    
    cleaned = "\n".join(cleaned_lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    
    return cleaned.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """
    Split text into overlapping fixed-size character chunks.
    
    Args:
        text: The cleaned document text
        chunk_size: Target chunk length in characters (default 500)
        overlap: How many characters each chunk shares with the next (default 100)
    
    Returns:
        A list of chunk strings.
    """
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be larger than overlap")
    
    chunks = []
    step = chunk_size - overlap
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if len(chunk) >= 100:  # drop tiny tail chunks that lack context
            chunks.append(chunk)
        start += step
    
    return chunks

if __name__ == "__main__":
    docs = load_documents(DOCUMENTS_DIR)
    print(f"Loaded {len(docs)} documents\n")
    
    cleaned_docs = {name: clean_document(text) for name, text in docs.items()}
    
    # Chunk each cleaned document, preserving source filename per chunk
    all_chunks = []  # list of (chunk_text, source_filename, chunk_index) tuples
    for filename, cleaned_text in cleaned_docs.items():
        chunks = chunk_text(cleaned_text, chunk_size=500, overlap=100)
        for idx, chunk in enumerate(chunks):
            all_chunks.append((chunk, filename, idx))
    
    print(f"Total chunks across all documents: {len(all_chunks)}")
    print(f"\nChunks per document:")
    chunk_counts = {}
    for _, src, _ in all_chunks:
        chunk_counts[src] = chunk_counts.get(src, 0) + 1
    for src in sorted(chunk_counts.keys()):
        print(f"  {src}: {chunk_counts[src]} chunks")
    
    # Inspect 5 random chunks
    random.seed(42)
    print("\n--- 5 random chunks for inspection ---")
    sample = random.sample(all_chunks, 5)
    for i, (chunk, src, idx) in enumerate(sample, 1):
        print(f"\n[Chunk {i}] Source: {src}, chunk #{idx}, length: {len(chunk)} chars")
        print("-" * 50)
        print(chunk)
        print("-" * 50)