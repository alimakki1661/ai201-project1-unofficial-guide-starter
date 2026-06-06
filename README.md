# The Unofficial Guide — Project 1

A RAG (Retrieval-Augmented Generation) system that makes student reviews of College of Staten Island Computer Science professors searchable. Users ask plain-language questions and get grounded answers drawn from real Rate My Professors reviews, with source attribution.

---

## Domain

My Unofficial Guide makes student reviews of College of Staten Island Computer Science professors searchable. This knowledge is valuable because it helps students make better decisions about which professors and courses fit their learning style before they register, and it's hard to find through official channels because college websites usually only show basic course descriptions, not honest student experiences about workload, grading, exams, feedback, or teaching quality.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|------------------|
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

All 10 documents come from Rate My Professors. The single-source coverage is a known limitation, discussed in the Failure Case Analysis section.

---

## Chunking Strategy

**Chunk size:** ~500 characters

**Overlap:** 100 characters

**Why these choices fit your documents:** My documents are short, opinion-based RMP reviews. Each review usually includes metadata (quality, difficulty, course code, attendance, grade) and a short paragraph of student opinion. A typical full review runs 300–600 characters. A chunk size of ~500 characters is large enough to keep most full reviews intact without merging multiple unrelated reviews together. The 100-character overlap is small because reviews are discrete units rather than continuous prose — it's there mainly to protect meaning if a review gets split mid-sentence at a chunk boundary. Before chunking, raw documents are cleaned to strip RMP boilerplate (UI labels, "Similar Professors" lists, "Thumbs up/down" footers, ad markers, "Helpful" button labels) while preserving the actual review text, ratings, course codes, and meaningful tag descriptors.

**Final chunk count:** 60 chunks across all 10 documents (after filtering out tail chunks shorter than 100 characters that lacked sufficient context).

**Critical preprocessing step — professor name prepending:** During Milestone 4 retrieval testing, I discovered that RMP reviews don't repeat the professor's name within review bodies, so chunks past the file header had no way to be matched to professor-name queries. To fix this, every chunk is prefixed with `Professor [Name] (Computer Science, CSI):` before embedding. Without this, retrieval failed on queries like "What do students think of Professor Rao?"

---

## Sample Chunks

Five representative chunks from the cleaned, prepended chunk set:

**Chunk 1 (source: `SafetJahaj_CS.txt`, chunk #1):**
> Professor Safet Jahaj (Computer Science, CSI):
> k: Yes
> Attendance not mandatory. he randomly raises his tone sometimes when he speaks & it's NOT because students aren't paying attention. He just does it. Simple HW, based on youtube. Boring lectures. reads straight from slides. but he tries to be funny. I appreciate the effort. Advertises the textbook reading but his choice of book is terrible

**Chunk 2 (source: `EdemacuKENNEDY_CS.txt`, chunk #2):**
> Professor Edemacu KENNEDY (Computer Science, CSI):
> you'll get an A
> Tough grader
> Group projects
> Lecture heavy
>
> Quality 5.0 / Difficulty 2.0 / CSC326 / May 21st, 2025 / For Credit: Yes / Attendance: Mandatory / Would Take Again: Yes / Grade: Not sure yet
> Professor Edemacu was super knowledgeable and his classes were somewhat engaging. He gives two quizzes and a group project before the final. The final was tough but it was open book and notes were allowed.

**Chunk 3 (source: `JunRao_CS.txt`, chunk #5):**
> Professor Jun Rao (Computer Science, CSI):
> Hilarious
>
> Quality 1.0 / Difficulty 3.0 / csc315 / May 19th, 2025
> honestly bros not even a bad guy hes just not good at teaching and just very condescending, i feel like within 220 and 315 lab i havent actually learned anything from him and he usually picks one guy to point out and bully which is a bit unofrt

**Chunk 4 (source: `LouisPetingi_CS.txt`, chunk #0):**
> Professor Louis Petingi (Computer Science, CSI):
> 4.2 / 5
> Overall Quality Based on 31 ratings
> Louis Petingi
> Professor in the Computer Science department at College of Staten Island
> 81% Would take again
> 2.7 Level of Difficulty
> Rating Distribution: Awesome 5: 18, Great 4: 9, Good 3: 1, OK 2: 0, Awful 1: 3

**Chunk 5 (source: `BrianoBruno_CS.txt`, chunk #2):**
> Professor Briano Bruno (Computer Science, CSI):
> Really great professor who genuinely cares about his students. Works in the field and gives practical advice. Class is engaging and labs are set up intentionally to help with the final project which was fun to create. Put in the effort and you will do great. Slideshows of class lectures were all shared and helpful. Would take Professor Bruno again!

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` (via `sentence-transformers`)

I'm using all-MiniLM-L6-v2 because it is free, runs locally, and is fast enough for a small class project with English Rate My Professors review text. Since my chunks are short and opinion-based, this model is strong enough to match student questions with related reviews even when the wording is not exactly the same. Retrieval uses top-k = 5: too few chunks (1 or 2) could miss useful reviews, while too many (10+) would give the LLM weakly related context and dilute the answer.

**Production tradeoff reflection:** If I were building this for real users, I would compare embedding models based on accuracy, cost, and latency. A larger API-based embedding model (such as OpenAI's `text-embedding-3-large` or Cohere's models) might understand more nuance in student reviews, but it would cost money per token and add network latency on each query. Context length is not a meaningful tradeoff for my current data because chunks are ~500 characters — well within any model's window. Multilingual support isn't relevant since all reviews are English. The most realistic upgrade for this domain would be a slightly larger English-focused open model (e.g., `bge-large-en`) that would still run locally but offer better semantic discrimination for the dense metadata-heavy chunks this data produces.

---

## Retrieval Test Results

Three test queries with their top retrieved chunks and explanations of why those chunks are relevant.

**Query 1: "Is attendance mandatory in Professor Jahaj's CSC220 course?"**

Top-3 retrieved (with distance):
1. `SafetJahaj_CS.txt` chunk #1 (0.663) — contains the literal phrase "Attendance not mandatory" for Jahaj's class
2. `JunRao_CS.txt` chunk #4 (0.691) — different professor but matches "Attendance: Mandatory" pattern
3. `JunRao_CS.txt` chunk #2 (0.732) — same generic "Attendance" pattern in a different professor's review

**Why these chunks are relevant:** The rank-1 chunk is highly relevant — it's the exact chunk containing the answer ("Attendance not mandatory" in a CSC220 Jahaj review). Ranks 2 and 3 are loosely relevant because they share the "Attendance" attribute that the query emphasizes, but they're from the wrong professor. This is expected behavior with semantic search on metadata-heavy chunks: the system found the right answer but also pulled false-positive matches based on shared attribute words.

**Query 2: "How does Professor Edemacu structure his CSC326 course?"**

Top-3 retrieved (with distance):
1. `EdemacuKENNEDY_CS.txt` chunk #2 (0.693) — contains "Group projects", "Lecture heavy", and the review describing "two quizzes and a group project before the final"
2. `EdemacuKENNEDY_CS.txt` chunk #1 (0.738) — another Edemacu CSC326 review mentioning grading style
3. `EdemacuKENNEDY_CS.txt` chunk #3 (0.830) — a third Edemacu chunk with course structure details

**Why these chunks are relevant:** All three top chunks come from the correct professor's file and reference CSC326 specifically. The professor name prepending (added during Milestone 4) is doing its job — the embedding model recognizes "Edemacu" + "CSC326" together and surfaces the right chunks. This is the kind of well-scoped, single-professor query where the system performs best.

**Query 3: "What do students think of Professor Rao?"**

Top-3 retrieved (with distance):
1. `JunRao_CS.txt` chunk #5 (0.677) — the harshest review ("not good at teaching", "condescending", "bully")
2. `JunRao_CS.txt` chunk #1 (0.824) — a positive outlier review ("genuinely just wants you to show up")
3. `JunRao_CS.txt` chunk #2 (0.927) — a milder critical review ("communication skills" complaint)

All 5 top chunks were from `JunRao_CS.txt`. This was the query I used to validate that the professor name prepending fix worked — before the fix, the top-5 contained zero Rao chunks. After the fix, all top-5 are Rao chunks.

---

## Grounded Generation

**System prompt grounding instruction:** The LLM (Groq's `llama-3.3-70b-versatile`) receives a system prompt that strictly limits its scope to retrieved context. Key rules in the prompt:

1. "Answer ONLY using information from the provided reviews. Do NOT use any outside knowledge about these professors or any other topic."
2. "If the reviews do not contain enough information to answer the question, respond exactly: 'I don't have enough information in the documents to answer that.'"
3. "Do not make up details, ratings, course codes, or facts that are not explicitly stated in the reviews."

Temperature is set to 0.2 (low) to further discourage creative elaboration. The user message includes the retrieved chunks labeled as "Document 1," "Document 2," etc., so the model can reference them by index.

**How source attribution is surfaced in the response:** Source attribution is surfaced programmatically rather than relying on the LLM. After retrieval, the system collects the unique source filenames from all top-k chunks and appends them to the response as a separate "Retrieved from" list. This is more reliable than asking the LLM to cite sources in prose, because the source list always reflects what was retrieved — even if the LLM didn't explicitly use every chunk. A known tradeoff: the source list shows all retrieved sources, not just the ones the LLM drew from, which means the list can include irrelevant files when retrieval pulls false positives (see Q1 in the Evaluation Report).

---

## Example Responses

**Example 1 — grounded answer with source attribution:**

**Question:** Is attendance mandatory in Professor Jahaj's CSC220 course?

**Answer:** According to the student reviews, attendance is not mandatory in Professor Jahaj's CSC220 course. This information is mentioned in two reviews (Document 1 and Document 5) for Professor Safet Jahaj's CSC220 course, both stating "Attendance: Not Mandatory".

**Retrieved from:**
- FatmaKausar_CS.txt
- JunRao_CS.txt
- SafetJahaj_CS.txt

---

**Example 2 — grounded answer with source attribution:**

**Question:** How does Professor Edemacu structure his CSC326 course?

**Answer:** According to the student reviews, Professor Edemacu structures his CSC326 course with the following elements:
- Lecture heavy
- Group projects
- Two quizzes before the final
- A final that is open book and notes are allowed.

**Retrieved from:**
- EdemacuKENNEDY_CS.txt
- PingShi_CS.txt

---

**Example 3 — out-of-scope refusal:**

**Question:** What is Professor Petingi's research area?

**Answer:** I don't have enough information in the documents to answer that.

**Retrieved from:**
- EdemacuKENNEDY_CS.txt
- LouisPetingi_CS.txt

The retrieved Petingi chunks discussed his teaching of CSC382 but never mentioned research. The LLM correctly refused rather than hallucinating from training data.

---

## Query Interface

The interface is a Gradio web UI launched from `app.py` and accessed at `http://localhost:7860`.

**Input field:**
- **Your question** — multi-line text box where the user types a question in plain English

**Output fields:**
- **Answer** — multi-line text box displaying the LLM-generated response
- **Retrieved from** — text box displaying the bulleted list of source filenames the retrieval returned

**Submit mechanism:** An "Ask" button (or pressing Enter) triggers retrieval + generation. The answer and sources update in place.

**Sample interaction transcript:**

```
[User enters in the question box]
Your question: Is Professor Jahaj's class easy?

[Clicks "Ask"]

Answer:
According to the student reviews, Professor Jahaj's class difficulty varies.
Some reviews state the difficulty as 1.0 (Document 2 and Document 5), 2.0
(Document 1), and 3.0 (Document 3), indicating that his class can be considered
easy to moderately difficult, depending on the course (CSC220 or CSC221) and
the student's perspective.

Retrieved from:
- SafetJahaj_CS.txt
- TatianaAnderson_CS.txt
```

---

## Evaluation Report

All 5 evaluation questions from `planning.md`, run end-to-end through the system. Full retrieval transcripts and chunk-level detail are in `evaluation_results.md`.

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Is attendance mandatory in Professor Jahaj's CSC220 course? | No — multiple reviews state attendance is not mandatory | Correctly answered "not mandatory," grounded in Jahaj chunk at rank 1 | Partially relevant (top-1 correct, ranks 2–3 wrong professor) | Accurate |
| 2 | How does Professor Edemacu structure his CSC326 course? | Two quizzes + group project before final; final is open-book with notes | Captured all expected elements plus "lecture heavy" and "mandatory attendance" | Relevant (3 of top-5 from correct file) | Accurate |
| 3 | How do students feel about Professor Rao? | Mostly negative; 1.9/5 rating; complaints re: communication, condescension, excessive testing | Characterized opinions as "mixed"; did not synthesize the 1.9/5 rating data | Relevant (all top-5 from Rao file) | Partially accurate |
| 4 | Which professors teach CSC326 at CSI? | Edemacu Kennedy and Tatiana Anderson | "I don't have enough information…" — refused incorrectly | Off-target (top results were wrong-course chunks) | Inaccurate |
| 5 | What is Professor Petingi's research area? | Should refuse — reviews don't discuss research | Correctly refused with the expected phrasing | Relevant (Petingi chunks retrieved, none contained research info) | Accurate |

**Summary:** 3/5 fully accurate, 1/5 partially accurate, 1/5 inaccurate (failure case).

---

## Failure Case Analysis

**Question that failed:** "Which professors teach CSC326 at CSI?"

**What the system returned:** "I don't have enough information in the documents to answer that."

**Root cause (tied to a specific pipeline stage):** This failure is rooted in the **retrieval stage**, specifically the limits of dense semantic search for keyword-precise queries. When searching for "CSC326," the embedding model considers the whole chunk's meaning, not just whether the substring "CSC326" appears. Many of my chunks share the general pattern "professor teaches CSC###," so chunks about CSC220, CSC315, and other course codes scored similarly to CSC326 chunks. The actual CSC326 chunks from Edemacu and Anderson didn't surface in the top-5 because they emphasize teaching style descriptors ("Group projects," "Tough grader") rather than the course code itself, weakening their embedding match against a course-code-focused query. The Tatiana Anderson chunk that *was* retrieved (rank 5) discussed CSC330, not CSC326, even though her file contains both. The LLM, seeing five top chunks none of which clearly answered the question, correctly refused.

**What you would change to fix it:** Add hybrid retrieval combining the current semantic search with BM25 keyword search. BM25 would directly match the literal string "CSC326" and surface those chunks regardless of their surrounding semantic content. This is one of the stretch features listed in the project spec, and would be the right next step for this system. A simpler intermediate fix would be to add explicit course-code metadata to each chunk during ingestion (extracting course codes via regex) and supporting a metadata filter at query time.

---

## Spec Reflection

**One way the spec helped me during implementation:** The chunking guidance in the spec — specifically the bullet point about how "review-style text may warrant smaller chunks than long-form guides" and the guiding questions about whether a key fact spans two chunks — made me think carefully about chunk size before I wrote any code. Without that prompt, I would have defaulted to a generic 1000-character chunk and split reviews mid-content. Because I'd thought through the structure of an RMP review first (300–600 characters per review, self-contained, metadata-heavy), the 500-character / 100-overlap choice I committed to in `planning.md` actually fit the data on first try — chunks aligned with reviews most of the time. The spec's insistence on writing this down *before* writing the code meant I had a defensible design to point back to when retrieval test results came in.

**One way my implementation diverged from the spec, and why:** My implementation added a step that wasn't in my original `planning.md`: prepending every chunk with `Professor [Name] (Computer Science, CSI):` before embedding. The original spec only said to attach professor name as metadata, but during Milestone 4 retrieval testing I discovered that semantic search couldn't match queries like "What do students think of Professor Rao?" — because RMP reviews don't repeat the professor's name within review bodies, so most chunks had no professor name in the embedding text itself. Metadata helps source attribution but doesn't influence the embedding similarity score. I diverged from the spec by injecting the professor name into the chunk text, which immediately fixed retrieval. This is documented in the Chunking Strategy section above.

---

## AI Usage

**Instance 1 — Document cleaning script (Milestone 3)**

- *What I gave the AI:* My `planning.md` Documents and Chunking Strategy sections, plus a sample of one raw RMP file. I asked Claude to write a Python function that removes RMP boilerplate (UI labels, "Similar Professors" lists, "Thumbs up/down" footers, ad markers) while preserving review text, ratings, course codes, and metadata.

- *What it produced:* A `clean_document()` function using a line-by-line pass with pattern matching and an index-based skip for multi-line blocks like "Similar Professors."

- *What I changed or overrode:* The first version had a bug — it skipped 11 lines after detecting "Similar Professors" when the actual block is 7 lines. This caused the first review of every file to lose its "Quality" and score lines, since they fell within the over-counted skip range. I caught the bug by inspecting the cleaned preview of `LouisPetingi_CS.txt`, told Claude exactly what was missing, and Claude produced the fix (changing 11 to 7 and adding a separate regex skip for the "N Student Ratings" line that had been incidentally caught by the over-count). I also directed the cleaning to *preserve* the rating distribution data (e.g., "Awesome 5: 18") because my Q3 evaluation question relies on it — the default would have been to treat that block as boilerplate.

**Instance 2 — Diagnosing and fixing retrieval failure on Q3 (Milestone 4)**

- *What I gave the AI:* The output of my first retrieval test where Q3 ("What do students think of Professor Rao?") returned zero JunRao chunks in the top-5. I shared the actual top-5 results showing chunks from Mohamed, Edemacu, and Bruno instead.

- *What it produced:* A diagnosis: RMP reviews don't repeat the professor's name within review bodies, so only chunk #0 of each file (containing the header) had the professor name in the embedding text. All other chunks lost the connection between the professor's name and the review content. Claude proposed prepending `Professor [Name] (Computer Science, CSI):` to every chunk before embedding, and rewrote the `build_chunk_list()` function to do so.

- *What I changed or overrode:* I accepted the diagnosis and fix as proposed, but I directed the change to be documented in `README.md` (Chunking Strategy section) and `Spec Reflection` (as a divergence from my original `planning.md`), since the fix wasn't in my original plan. I also tested the fix on all three of my Milestone 4 retrieval queries before moving on, which confirmed Jahaj (Q1), Edemacu (Q2), and Rao (Q3) all removed.

---

## Failure Case Analysis

**Question that failed:** "Which professors teach CSC326 at CSI?"

**What the system returned:** "I don't have enough information in the documents to answer that."

**Root cause (tied to a specific pipeline stage):** This failure is rooted in the **retrieval stage**, specifically the limits of dense semantic search for keyword-precise queries. When searching for "CSC326," the embedding model considers the whole chunk's meaning, not just whether the substring "CSC326" appears. Many of my chunks share the general pattern "professor teaches CSC###," so chunks about CSC220, CSC315, and other course codes scored similarly to CSC326 chunks. The actual CSC326 chunks from Edemacu and Anderson didn't surface in the top-5 because they emphasize teaching style descriptors ("Group projects," "Tough grader") rather than the course code itself, weakening their embedding match against a course-code-focused query. The Tatiana Anderson chunk that *was* retrieved (rank 5) discussed CSC330, not CSC326, even though her file contains both. The LLM, seeing five top chunks none of which clearly answered the question, correctly refused.

**What you would change to fix it:** Add hybrid retrieval combining the current semantic search with BM25 keyword search. BM25 would directly match the literal string "CSC326" and surface those chunks regardless of their surrounding semantic content. This is one of the stretch features listed in the project spec, and would be the right next step for this system. A simpler intermediate fix would be to add explicit course-code metadata to each chunk during ingestion (extracting course codes via regex) and supporting a metadata filter at query time.

---

## Spec Reflection

**One way the spec helped me during implementation:** The chunking guidance in the spec — specifically the bullet point about how "review-style text may warrant smaller chunks than long-form guides" and the guiding questions about whether a key fact spans two chunks — made me think carefully about chunk size before I wrote any code. Without that prompt, I would have defaulted to a generic 1000-character chunk and split reviews mid-content. Because I'd thought through the structure of an RMP review first (300–600 characters per review, self-contained, metadata-heavy), the 500-character / 100-overlap choice I committed to in `planning.md` actually fit the data on first try — chunks aligned with reviews most of the time. The spec's insistence on writing this down *before* writing the code meant I had a defensible design to point back to when retrieval test results came in.

**One way my implementation diverged from the spec, and why:** My implementation added a step that wasn't in my original `planning.md`: prepending every chunk with `Professor [Name] (Computer Science, CSI):` before embedding. The original spec only said to attach professor name as metadata, but during Milestone 4 retrieval testing I discovered that semantic search couldn't match queries like "What do students think of Professor Rao?" — because RMP reviews don't repeat the professor's name within review bodies, so most chunks had no professor name in the embedding text itself. Metadata helps source attribution but doesn't influence the embedding similarity score. I diverged from the spec by injecting the professor name into the chunk text, which immediately fixed retrieval. This is documented in the Chunking Strategy section above.

---

## AI Usage

**Instance 1 — Document cleaning script (Milestone 3)**

- *What I gave the AI:* My `planning.md` Documents and Chunking Strategy sections, plus a sample of one raw RMP file. I asked Claude to write a Python function that removes RMP boilerplate (UI labels, "Similar Professors" lists, "Thumbs up/down" footers, ad markers) while preserving review text, ratings, course codes, and metadata.

- *What it produced:* A `clean_document()` function using a line-by-line pass with pattern matching and an index-based skip for multi-line blocks like "Similar Professors."

- *What I changed or overrode:* The first version had a bug — it skipped 11 lines after detecting "Similar Professors" when the actual block is 7 lines. This caused the first review of every file to lose its "Quality" and score lines, since they fell within the over-counted skip range. I caught the bug by inspecting the cleaned preview of `LouisPetingi_CS.txt`, told Claude exactly what was missing, and Claude produced the fix (changing 11 to 7 and adding a separate regex skip for the "N Student Ratings" line that had been incidentally caught by the over-count). I also directed the cleaning to *preserve* the rating distribution data (e.g., "Awesome 5: 18") because my Q3 evaluation question relies on it — the default would have been to treat that block as boilerplate.

**Instance 2 — Diagnosing and fixing retrieval failure on Q3 (Milestone 4)**

- *What I gave the AI:* The output of my first retrieval test where Q3 ("What do students think of Professor Rao?") returned zero JunRao chunks in the top-5. I shared the actual top-5 results showing chunks from Mohamed, Edemacu, and Bruno instead.

- *What it produced:* A diagnosis: RMP reviews don't repeat the professor's name within review bodies, so only chunk #0 of each file (containing the header) had the professor name in the embedding text. All other chunks lost the connection between the professor's name and the review content. Claude proposed prepending `Professor [Name] (Computer Science, CSI):` to every chunk before embedding, and rewrote the `build_chunk_list()` function to do so.

- *What I changed or overrode:* I accepted the diagnosis and fix as proposed, but I directed the change to be documented in `README.md` (Chunking Strategy section) and `Spec Reflection` (as a divergence from my original `planning.md`), since the fix wasn't in my original plan. I also tested the fix on all three of my Milestone 4 retrieval queries before moving on, which confirmed Jahaj (Q1), Edemacu (Q2), and Rao (Q3) all improved.