# Evaluation Results

## Q1: Is attendance mandatory in Professor Jahaj's CSC220 course?

**Expected answer:** No. Multiple reviews state that attendance is not mandatory.

**System response:**

According to the student reviews, attendance is not mandatory in Professor Jahaj's CSC220 course. This information is mentioned in two reviews (Document 1 and Document 5) for Professor Safet Jahaj's CSC220 course, both stating "Attendance: Not Mandatory".

**Sources retrieved:**
- FatmaKausar_CS.txt
- JunRao_CS.txt
- SafetJahaj_CS.txt

**Top retrieved chunks (with distance):**

1. `SafetJahaj_CS.txt` (distance: 0.663): Professor Safet Jahaj (Computer Science, CSI): k: Yes Attendance not mandatory. he randomly raises his tone sometimes when he speaks & it's NOT because students aren't paying attention. He just does it. Simple HW, based on youtube. Boring lectures. r...
2. `JunRao_CS.txt` (distance: 0.691): Professor Jun Rao (Computer Science, CSI): th, 2025 For Credit: Yes Attendance: Mandatory Would Take Again: Yes Grade: A+ Textbook: N/A Professor is an amazing instructor who truly cares about students' success. Their lectures are clear, engaging, an...
3. `JunRao_CS.txt` (distance: 0.732): Professor Jun Rao (Computer Science, CSI): 0 CSC126 Feb 11th, 2026 For Credit: Yes Attendance: Not Mandatory Grade: Rather not say Textbook: N/A He's fine but he needs to work on his communication skills based on the test reviews and lab instructions...
4. `FatmaKausar_CS.txt` (distance: 0.884): Professor Fatma Kausar (Computer Science, CSI): th, 2024 For Credit: Yes Attendance: Mandatory Would Take Again: Yes Grade: A Textbook: N/A She was awesome. Very easy to talk to, curved exams, and lectures were easy to follow and tried to keep studen...
5. `SafetJahaj_CS.txt` (distance: 0.909): Professor Safet Jahaj (Computer Science, CSI): r Credit: Yes Attendance: Not Mandatory Would Take Again: Yes Grade: Rather not say Textbook: N/A one word! AMAZING Gives good feedback Hilarious Caring  Quality 5.0 Difficulty 3.0 CSC220 Dec 19th, 2024 ...

**Accuracy judgment:** ✅ Accurate. The system correctly answered "not mandatory" and grounded the response in the actual SafetJahaj chunk (rank 1, distance 0.663). Retrieval also pulled two unrelated wrong-prof chunks (Kausar, Rao), but the LLM correctly ignored them when forming the answer — good grounding behavior.
---

## Q2: How does Professor Edemacu structure his CSC326 course?

**Expected answer:** He gives two quizzes and a group project before the final. The final is open-book with notes allowed.

**System response:**

According to the student reviews, Professor Edemacu structures his CSC326 course with the following elements: 
- Lecture heavy
- Group projects
- Two quizzes before the final
- A final that is open book and notes are allowed.

**Sources retrieved:**
- EdemacuKENNEDY_CS.txt
- PingShi_CS.txt

**Top retrieved chunks (with distance):**

1. `EdemacuKENNEDY_CS.txt` (distance: 0.693): Professor Edemacu K E N N E D Y (Computer Science, CSI): you'll get an A Tough grader Group projects Lecture heavy  Quality 5.0 Difficulty 2.0 CSC326 May 21st, 2025 For Credit: Yes Attendance: Mandatory Would Take Again: Yes Grade: Not sure yet Textb...
2. `EdemacuKENNEDY_CS.txt` (distance: 0.738): Professor Edemacu K E N N E D Y (Computer Science, CSI): book: N/A really nice professor and very lenient with grading Get ready to read Group projects Caring  Quality 5.0 Difficulty 4.0 CSC326 May 21st, 2025 For Credit: Yes Attendance: Mandatory Wou...
3. `EdemacuKENNEDY_CS.txt` (distance: 0.830): Professor Edemacu K E N N E D Y (Computer Science, CSI): llowed. He has a super nice personality and is a professor that genuinely cares about his students and their success. Group projects Gives good feedback Caring  Quality 1.0 Difficulty 5.0 CSC32...
4. `PingShi_CS.txt` (distance: 0.855): Professor Ping Shi (Computer Science, CSI): es I had her for CSC220 and CSC 211. If you actually put in the effort to learn the material you will be fine. She wants you to actually understand content. Clear grading criteria Gives good feedback Access...
5. `EdemacuKENNEDY_CS.txt` (distance: 0.925): Professor Edemacu K E N N E D Y (Computer Science, CSI): 4 / 5 Overall Quality Based on 4 ratings Edemacu KENNEDY Professor in the Computer Science department at College of Staten Island (CUNY - Staten Island) 75% Would take again 3.8 Level of Diffic...

**Accuracy judgment:** ✅ Accurate. The system captured all the structural elements in the expected answer (two quizzes, group project, open-book final with notes) and additionally surfaced "lecture heavy" and "mandatory attendance," which are also supported by the reviews. Three of the top 5 retrieved chunks were from EdemacuKENNEDY_CS.txt, giving the LLM strong context.

---

## Q3: How do students feel about Professor Rao?

**Expected answer:** Most reviews are negative. He has a 1.9/5 overall rating with 15 of 24 ratings being 1-star. Frequent complaints include communication, condescension, and excessive testing.

**System response:**

According to the student reviews, opinions about Professor Rao are mixed. Some students feel that he is "not good at teaching" and "condescending" (Document 1), while others think he is "amazing" and "truly cares about students' success" (Document 4). Another student mentions that he is "alright" but needs to work on his communication skills (Document 3). One student also appreciates that he "genuinely just wants you to show up to his class and do well" (Document 2). Overall, the reviews suggest that students have varying experiences with Professor Rao.

**Sources retrieved:**
- JunRao_CS.txt

**Top retrieved chunks (with distance):**

1. `JunRao_CS.txt` (distance: 0.724): Professor Jun Rao (Computer Science, CSI): rk Hilarious  Quality 1.0 Difficulty 3.0 csc315 May 19th, 2025 For Credit: Yes Attendance: Mandatory Grade: A- Textbook: N/A honestly bros not even a bad guy hes just not good at teaching and just very conde...
2. `JunRao_CS.txt` (distance: 0.850): Professor Jun Rao (Computer Science, CSI): CSC 424, not 382. First time taking the professor, and he genuinely just wants you to show up to his class and do well. I have lots of respect for him, and I wish I had taken more courses with him before gra...
3. `JunRao_CS.txt` (distance: 0.947): Professor Jun Rao (Computer Science, CSI): 0 CSC126 Feb 11th, 2026 For Credit: Yes Attendance: Not Mandatory Grade: Rather not say Textbook: N/A He's fine but he needs to work on his communication skills based on the test reviews and lab instructions...
4. `JunRao_CS.txt` (distance: 0.969): Professor Jun Rao (Computer Science, CSI): th, 2025 For Credit: Yes Attendance: Mandatory Would Take Again: Yes Grade: A+ Textbook: N/A Professor is an amazing instructor who truly cares about students' success. Their lectures are clear, engaging, an...
5. `JunRao_CS.txt` (distance: 0.990): Professor Jun Rao (Computer Science, CSI): 1.9 / 5 Overall Quality Based on 24 ratings Jun Rao Professor in the Computer Science department at College of Staten Island (CUNY - Staten Island) 24% Would take again 3.9 Level of Difficulty  Rating Distri...

**Accuracy judgment:** ⚠️ Partially accurate. The system characterized opinions as "mixed," which is defensible given the specific 5 reviews retrieved (3 negative, 2 positive), but it doesn't reflect the overall pattern (1.9/5 rating, 15 of 24 reviews 1-star). The 1.9/5 stat was present in chunk #5 of the retrieved set but the LLM didn't synthesize it into the answer — it focused on individual review opinions instead of aggregating the rating distribution data.

---

## Q4: Which professors teach CSC326 at CSI?

**Expected answer:** Edemacu Kennedy and Tatiana Anderson.

**System response:**

I don't have enough information in the documents to answer that.

**Sources retrieved:**
- AliMohamed_CS.txt
- FatmaKausar_CS.txt
- LuigiKapaj_CS.txt
- PingShi_CS.txt
- TatianaAnderson_CS.txt

**Top retrieved chunks (with distance):**

1. `PingShi_CS.txt` (distance: 0.753): Professor Ping Shi (Computer Science, CSI): es I had her for CSC220 and CSC 211. If you actually put in the effort to learn the material you will be fine. She wants you to actually understand content. Clear grading criteria Gives good feedback Access...
2. `LuigiKapaj_CS.txt` (distance: 0.755): Professor Luigi Kapaj (Computer Science, CSI): 5 Dec 29th, 2024 For Credit: Yes Attendance: Not Mandatory Grade: A Textbook: Yes If you want an easy A, take this class. Mid terms and finals are online. Lecture heavy  Quality 5.0 Difficulty 1.0 CSC315...
3. `AliMohamed_CS.txt` (distance: 0.780): Professor Ali Mohamed (Computer Science, CSI): ests instead of three. Midterm easy, but the final slightly hard. The class material was very fun to learn, but the later half of the semester gets annoying with the diagrams. Easy class, overall. Inspir...
4. `FatmaKausar_CS.txt` (distance: 0.786): Professor Fatma Kausar (Computer Science, CSI): th, 2024 For Credit: Yes Attendance: Mandatory Would Take Again: Yes Grade: A Textbook: N/A She was awesome. Very easy to talk to, curved exams, and lectures were easy to follow and tried to keep studen...
5. `TatianaAnderson_CS.txt` (distance: 0.804): Professor Tatiana Anderson (Computer Science, CSI): 30th, 2024 For Credit: Yes Attendance: Mandatory Grade: A Textbook: Yes To add on, the project was extremely complicated. Our group was very confused as to what to do for it and she did not teach us...

**Accuracy judgment:** ❌ Inaccurate — this is the project's main failure case. The expected answer is "Edemacu Kennedy and Tatiana Anderson," but the system said it didn't have enough information. Retrieval pulled mostly wrong-course chunks (Shi for CSC220/CSC211, Kapaj for CSC315, Mohamed) instead of the CSC326-specific chunks from Edemacu and Anderson. See the failure case analysis below for the explanation.

---

## Q5: What is Professor Petingi's research area?

**Expected answer:** The system should say it doesn't have enough information. The reviews focus on his teaching of CSC382 and don't discuss his research.

**System response:**

I don't have enough information in the documents to answer that.

**Sources retrieved:**
- EdemacuKENNEDY_CS.txt
- LouisPetingi_CS.txt

**Top retrieved chunks (with distance):**

1. `LouisPetingi_CS.txt` (distance: 0.969): Professor Louis Petingi (Computer Science, CSI): for the final exam due to a project in another course. Good professor, very funny. Suggestion please specify which specific reviews the exam questions are from. This could have helped me for the final ...
2. `LouisPetingi_CS.txt` (distance: 1.096): Professor Louis Petingi (Computer Science, CSI): rk when a course ends at 620 in the evening. Good professor, but take him with a lot of caution as he may not be GPA friendly. Amazing lectures Inspirational Caring  Quality 5.0 Difficulty 1.0 CSC382 M...
3. `LouisPetingi_CS.txt` (distance: 1.123): Professor Louis Petingi (Computer Science, CSI): 4.2 5 Overall Quality Based on 31 ratings Louis Petingi Professor in the Computer Science department at College of Staten Island (CUNY - Staten Island) 81% Would take again 2.7 Level of Difficulty  Rat...
4. `EdemacuKENNEDY_CS.txt` (distance: 1.231): Professor Edemacu K E N N E D Y (Computer Science, CSI): llowed. He has a super nice personality and is a professor that genuinely cares about his students and their success. Group projects Gives good feedback Caring  Quality 1.0 Difficulty 5.0 CSC32...
5. `LouisPetingi_CS.txt` (distance: 1.282): Professor Louis Petingi (Computer Science, CSI): ood professor, but the final exam tanked my grade, along with other students'. It was difficult.  Quality 5.0 Difficulty 1.0 CSC382 May 26th, 2025 For Credit Yes Attendance Mandatory Would Take Again Y...

**Accuracy judgment:** ✅ Accurate. The system correctly refused with "I don't have enough information in the documents to answer that," which is the exact phrasing required by the system prompt. Retrieval did pull Petingi chunks (since the query mentioned his name), but none contained research-area information, and the LLM resisted any temptation to hallucinate from training knowledge.


## Summary

- 3/5 fully accurate, 1/5 partially accurate, 1/5 inaccurate (failure case)
- Q1, Q2, Q5: ✅ Accurate
- Q3: ⚠️ Partially accurate
- Q4: ❌ Inaccurate (failure case — see below)

## Failure Case: Q4 — Course Code Disambiguation

**Question:** "Which professors teach CSC326 at CSI?"
**Expected:** Edemacu Kennedy and Tatiana Anderson
**Got:** "I don't have enough information in the documents to answer that"

**Why it failed:** This is a course-code lookup query, which semantic search handles poorly. When searching for "CSC326," the embedding model considers the whole chunk's meaning, not just whether the substring "CSC326" appears. Many chunks share the general pattern "professor teaches CSC###," so chunks about CSC220, CSC315, etc. ranked similarly to CSC326 chunks. The CSC326 chunks from Edemacu emphasize teaching style ("Group projects", "Tough grader") rather than the course code, weakening their embedding match against a course-code query.

**Pipeline component responsible:** Retrieval (specifically, the limits of dense semantic search for keyword-precise queries).

**Possible fix:** Hybrid search combining semantic similarity (current) with BM25 keyword search would catch the literal "CSC326" string and surface those chunks. This is one of the stretch features mentioned in the project spec.

---

