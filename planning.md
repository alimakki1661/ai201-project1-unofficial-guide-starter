# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

 My Unofficial Guide makes student reviews of College of Staten Island Computer Science professors searchable. This knowledge is valuable because it helps students make better decisions about which professors and courses fit their learning style before they register, and it's hard to find through official channels because college websites usually only show basic course descriptions, not honest student experiences about workload, grading, exams, feedback, or teaching quality.

---

## Documents


| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors | Edemacu Kennedy — CSC326 reviews (4 ratings) | documents/EdemacuKENNEDY_CS.txt |
| 2 | Rate My Professors | Fatma Kausar — CSC126 reviews (6 ratings) | documents/FatmaKausar_CS.txt |
| 3 | Rate My Professors | Louis Petingi — CSC382 reviews (31 ratings, 5 collected) | documents/LouisPetingi_CS.txt |
| 4 | Rate My Professors | Tatiana Anderson — CSC326 and CSC330 reviews (34 ratings, 5 collected) | documents/TatianaAnderson_CS.txt |
| 5 | Rate My Professors | Safet Jahaj — CSC220 and CSC221 reviews (16 ratings, 5 collected) | documents/SafetJahaj_CS.txt |
| 6 | Rate My Professors | Luigi Kapaj — CSC315 reviews (11 ratings, 5 collected) | documents/LuigiKapaj_CS.txt |
| 7 | Rate My Professors | Jun Rao — CSC126, CSC220, CSC315, CSC382 reviews (24 ratings, 5 collected) | documents/JunRao_CS.txt |
| 8 | Rate My Professors | Briano Bruno — CSC225 reviews (5 ratings) | documents/BrianoBruno_CS.txt |
| 9 | Rate My Professors | Ping Shi — CSC211, CSC220, CSC446 reviews (76 ratings, 5 collected) | documents/PingShi_CS.txt |
| 10 | Rate My Professors | Ali Mohamed — CSC220, CSC346, CSC347, CSC446 reviews (21 ratings, 10 collected) | documents/AliMohamed_CS.txt |
---

## Chunking Strategy

**Chunk size:** ~500 characters

**Overlap:** 100 characters

**Reasoning:** My documents are Rate My Professors reviews for CSI Computer Science professors. The reviews are short, opinion-based, and mostly self-contained. Each review usually includes metadata like quality, difficulty, course code, attendance, grade, and then a short paragraph explaining the student's experience.

A typical review with its metadata and opinion text is usually around 300–600 characters. I chose a chunk size of about 500 characters because that is large enough to keep most full reviews together without mixing too many unrelated reviews into one chunk. This should help the system retrieve specific student opinions about things like workload, grading, exams, attendance, and teaching style.

I chose a small overlap of 100 characters because these reviews are separate entries, not long essays where ideas continue across many paragraphs. The overlap is mainly there to protect meaning if a review gets split in the middle, but it is small enough to avoid repeating too much duplicate text.

If a review happens to be longer than 500 characters (a few of mine push toward 600), the tail end may get split into its own chunk with less context — I'll watch for this when I inspect chunks in Milestone 3.

---

## Retrieval Approach

**Embedding model:** all-MiniLM-L6-v2 through sentence-transformers 
 
**Top-k:** 5 
 
**Reasoning:** 
I am using all-MiniLM-L6-v2 because it is free, runs locally, and is fast enough for a small class project with English Rate My Professor review text. Since my chunks are short and opinion based, this model should be strong enough to match student questions with related reviews even when the wording is not exactly the same. I chose top-k = 5 because retrieving only 1 or 2 chunks could miss useful reviews, while retrieving 10 or more could give the LLM too much weakly related context and make the answer less focused. 
 
**Production tradeoffs:** 
If I were building this for real users, I would compare embedding models based on accuracy, cost, and latency. A larger API based embedding model might understand more nuance in student reviews, but it would cost money per token and depend on network calls. I would also consider context length, but because my chunks are around 500 characters, a very long context embedding model is not necessary for this version.

---

## Evaluation Plan

**Q1:** Is attendance mandatory in Professor Jahaj's course CSC220?
**Expected answer:** No. Multiple reviews state that attendance is not mandatory.

**Q2:** How does Professor Edemacu structure his CSC326 course?
**Expected answer:** He gives two quizzes and a group project before the final. The final is open-book with notes allowed.

**Q3:** How do students feel about Professor Rao?
**Expected answer:** Most reviews are negative. He has a 1.9/5 overall rating with 15 of 24 ratings being 1-star. Frequent complaints include communication, condescension, and excessive testing.

**Q4:** Which professors teach CSC326 at CSI?
**Expected answer:** Edemacu Kennedy and Tatiana Anderson.

**Q5:** What is Professor Petingi's research area?
**Expected answer:** The system should say it doesn't have enough information. The reviews focus on his teaching of CSC382 and don't discuss his research.

## Anticipated Challenges
1. **Single-source bias from Rate My Professors.**
All 10 of my documents are from RMP. RMP usually attracts a certain type of student — people who feel strongly enough to post a review. This means the system will miss perspectives from students who don't post on RMP, like opinions shared in Reddit threads, Discord servers, or word of mouth.

2. **Cross-course confusion within one professor's file.**
Many of the professors have multiple courses in one file. If a chunk ends up spanning two reviews from different courses, the system could mix up which course an opinion is about. For example, a query about CSC211 might pull a chunk with a CSC220 opinion attached.

3. **Generic RMP tag words dilute retrieval.**
Many reviews end with the same tag words like "Helpful," "Caring," and "Lecture heavy." These tags appear in a lot of chunks, so they don't discriminate between professors. A query like "which professor is helpful?" could retrieve almost any chunk.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 1: DOCUMENT INGESTION                                    │
│  Load raw .txt files from documents/ folder                     │
│  Tool: Python file I/O                                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 2: CHUNKING                                              │
│  Clean RMP boilerplate, split into ~500-char chunks             │
│  with 100-char overlap                                          │
│  Tool: Python (custom cleaning + chunking functions)            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 3: EMBEDDING + VECTOR STORE                              │
│  Embed chunks, store with metadata (source, professor, chunk #) │
│  Tools: sentence-transformers (all-MiniLM-L6-v2) + ChromaDB     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 4: RETRIEVAL                                             │
│  User query → embed → semantic search → top-5 chunks            │
│  Tool: ChromaDB similarity search                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 5: GROUNDED GENERATION                                   │
│  Send top-5 chunks + query + grounding prompt → answer + sources│
│  Tools: Groq API (llama-3.3-70b-versatile) + Gradio UI          │
└─────────────────────────────────────────────────────────────────┘
```
---

## AI Tool Plan

1. **Document cleaning script (Milestone 3):**
I will give Claude my Documents section, my Chunking Strategy section, and a sample of one of my raw Rate My Professors files. I will ask it to write a Python function that removes repeated RMP boilerplate, ads, navigation text, buttons, and unnecessary labels while keeping the professor name, department, overall rating, course code, quality/difficulty scores, and actual student review text. I will review the output to make sure useful content (review text, ratings, course codes) is kept and clutter (AD markers, "Similar Professors" lists, Thumbs up/down lines) is removed. I'll specifically check that the rating distribution data is preserved since one of my evaluation questions relies on it.

2. **Chunking implementation (Milestone 3):**
I will give Claude my Chunking Strategy section and ask it to write a function that splits cleaned documents into chunks of about 500 characters with 100 characters of overlap. I will inspect at least 5 chunks afterward to confirm they are readable, self-contained, and contain complete student-review information rather than broken fragments.

3. **Embedding and ChromaDB setup (Milestone 4):**
I will give Claude my Retrieval Approach section and pipeline diagram and ask it to write code that loads the cleaned chunks, embeds them with all-MiniLM-L6-v2, and stores them in ChromaDB. Each stored chunk should include metadata such as the source filename, professor name if available, and chunk number so retrieved answers can cite where the information came from.

4. **Retrieval function (Milestone 4):**
I will give Claude my Retrieval Approach section and ask it to write a function that takes a user query string and returns the top 5 most relevant chunks. The function should return each chunk's text, similarity score or distance score, and source metadata so I can inspect retrieval quality before adding the LLM.

5. **Generation and Gradio UI (Milestone 5):**
I will give Claude my Evaluation Plan questions, my grounding requirement, and the project instructions for source attribution. I will ask it to write code that sends the top retrieved chunks to the Groq API, generates an answer using only those chunks, and returns both the answer and the source list in a Gradio interface. I will review the system prompt to make sure it clearly tells the model not to use outside knowledge and to say it does not have enough information when the retrieved documents do not answer the question.