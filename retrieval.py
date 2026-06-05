"""
retrieval.py — Embedding, vector store, and retrieval for The Unofficial Guide
Milestone 4: embed chunks → store in ChromaDB → retrieve top-k by query
"""

import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_documents, clean_document, chunk_text, DOCUMENTS_DIR


# Constants
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "csi_cs_reviews"
TOP_K = 5


def build_chunk_list() -> list[tuple[str, str, int]]:
    """
    Run the full ingestion pipeline (load → clean → chunk).
    
    Prepends a "Professor: <name>" header to every chunk so the professor name
    appears in every embedding — without this, chunks past the file header lose
    the professor's name and retrieval can't match queries that name a professor.
    """
    docs = load_documents(DOCUMENTS_DIR)
    cleaned_docs = {name: clean_document(text) for name, text in docs.items()}
    
    all_chunks = []
    for filename, cleaned_text in cleaned_docs.items():
        # Extract professor name from the filename
        # e.g. "JunRao_CS.txt" → "Jun Rao", "EdemacuKENNEDY_CS.txt" → "Edemacu KENNEDY"
        base = filename.replace("_CS.txt", "")
        # Split CamelCase: "JunRao" → "Jun Rao"
        prof_name = ""
        for ch in base:
            if ch.isupper() and prof_name and not prof_name.endswith(" "):
                prof_name += " "
            prof_name += ch
        prof_name = prof_name.strip()
        
        # Prepend professor name to every chunk so it's in every embedding
        prefix = f"Professor {prof_name} (Computer Science, CSI):\n"
        
        chunks = chunk_text(cleaned_text, chunk_size=500, overlap=100)
        for idx, chunk in enumerate(chunks):
            prefixed_chunk = prefix + chunk
            all_chunks.append((prefixed_chunk, filename, idx))
    
    return all_chunks


def build_vector_store():
    """
    Embed all chunks and store them in a fresh ChromaDB collection.
    
    Returns the ChromaDB collection object, ready for querying.
    """
    print(f"Loading embedding model ({EMBEDDING_MODEL})...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    print("Building chunk list from documents...")
    all_chunks = build_chunk_list()
    print(f"  → {len(all_chunks)} chunks ready")
    
    # Initialize ChromaDB client (in-memory, no disk persistence for now)
    client = chromadb.Client()
    
    # Delete the collection if it already exists (so re-runs start fresh)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # collection didn't exist, that's fine
    
    collection = client.create_collection(name=COLLECTION_NAME)
    
    # Prepare data for batch insertion
    chunk_texts = [chunk for chunk, _, _ in all_chunks]
    ids = [f"{src}_chunk{idx}" for _, src, idx in all_chunks]
    metadatas = [
        {"source": src, "chunk_index": idx}
        for _, src, idx in all_chunks
    ]
    
    print("Embedding chunks (this may take a few seconds)...")
    embeddings = model.encode(chunk_texts).tolist()
    
    print("Storing in ChromaDB...")
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunk_texts,
        metadatas=metadatas,
    )
    
    print(f"  → {collection.count()} chunks stored in collection '{COLLECTION_NAME}'\n")
    return collection, model


def retrieve(collection, model, query: str, k: int = TOP_K) -> list[dict]:
    """
    Retrieve the top-k most relevant chunks for a query.
    
    Returns a list of dicts, each with: text, source, chunk_index, distance.
    """
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
    )
    
    # Unpack results into a friendlier shape
    retrieved = []
    for i in range(len(results["ids"][0])):
        retrieved.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
            "distance": results["distances"][0][i],
        })
    
    return retrieved


if __name__ == "__main__":
    collection, model = build_vector_store()
    
    # Test queries — using 3 of your 5 evaluation questions from planning.md
    test_queries = [
        "Is attendance mandatory in Professor Jahaj's CSC220 course?",
        "How does Professor Edemacu structure his CSC326 course?",
        "What do students think of Professor Rao?",
    ]
    
    for query in test_queries:
        print(f"\n{'=' * 70}")
        print(f"QUERY: {query}")
        print(f"{'=' * 70}")
        
        results = retrieve(collection, model, query, k=TOP_K)
        
        for rank, r in enumerate(results, 1):
            print(f"\n[Rank {rank}] Source: {r['source']}, chunk #{r['chunk_index']}, distance: {r['distance']:.3f}")
            print("-" * 70)
            # Print first 300 chars of chunk for readability
            preview = r["text"][:300] + ("..." if len(r["text"]) > 300 else "")
            print(preview)