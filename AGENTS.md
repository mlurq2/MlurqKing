# LectureKing Medical School Anki System Rules

This project workspace builds high-yield medical school flashcards from lecture slides and transcripts using the 4-Agent LectureKing pipeline.

## Architecture Standards: v1 (OG) vs. v2 vs. v2.1

This workspace supports three distinct architectures documented in `PIPELINE_SPECS.md`:

1. **v1 (OG / Classic Architecture):**
   * High-density, exhaustive slide-by-slide transcription (~2.5–4 cards/min).
   * ~85–90% single-cloze (`c1` default).
   * Formal academic textbook phrasing.
   * Strict minimum 3–4 semantic colors per sentence.
   * Use when the user requests: **`run v1`**, **`run OG`**, or **`use classic architecture`**.

2. **v2 (Natural Clinician & Student-Tested Tone Architecture):**
   * High-yield exam mastery; transcript is primary clinical truth, slides provide context.
   * Organic density driven by clinical pivots (no arbitrary hard caps).
   * "Natural Dyad Standard": Single `c1` default for standalone facts; buryable `c1`/`c2` pairs (max `c2`, zero `c3`) for natural twins (baselines vs cutoffs, indications vs contraindications, reciprocal switches, twin entities).
   * "Student-Tested Tone": Phrased in direct, plain clinical English (the way a top medical student writes cards for peers); fast 6–8 second reflex testing; zero flowery textbook jargon.
   * Opportunistic 5-color palette: apply colors naturally to existing terms; NEVER pad sentences to satisfy color quotas.
   * Use when the user requests: **`run v2`**.

3. **v2.1 (Transcript-Gated & Classmate-Refined Architecture):**
   * Built on the full v2 foundation (natural dyads, 6–8s reflex tone, zero `c3`).
   * **Transcript-Gated Filter & Endorsement Rule (Agent 1):** The transcript is the strict gatekeeper of testability. If a bullet point is on a slide but the professor gives it 0 seconds in the audio, DROP IT. Exception: if the professor verbally points to a table/diagram and says *"know this"* or *"this is on the exam"*, all items in that table/slide are fair game.
   * **The AnKing Gold Standard: Vignette-to-Punchline Clozing (Agent 2):** ~85–90% single `c1` cards. Front stems provide the patient scenario, risk factors, and exposures as un-clozed clinical clues, clozing ONLY the single testable punchline (diagnosis, first-line drug, unique stain, or cutoff). Never test trivia clues in isolation.
   * **Strict 10–15% Ceiling on `c1`/`c2` Dyads (Agent 2):** Reserve buryable `c1`/`c2` strictly for true reciprocal dualities (e.g. 25°C mold vs 37°C yeast; 45° septate vs 90° non-septate; acute intubation vs BVM contraindicated). Facts from the same disease entity (e.g. symptom + treatment) must NEVER be paired as a dyad.
   * **Strict Slide-Transcript Boundary on Fronts (Agent 2):** Front stems test ONLY the direct relationship established on the slide or in the audio (e.g. *"Coal worker's pneumoconiosis carries a high risk of developing {{c1::Caplan syndrome}}"*). NEVER import outside textbook definitions or deep pathophysiology onto the Front.
   * **The Medical Noun Anchor Rule (SuperMemo Rules 10 & 12) (Agent 2):** Never prune key medical nouns, specific cell types, diagnostic parameters, exposures, or dual lab markers (e.g. keep *epithelioid macrophages*, *crystalline silica*, *hypercalciuria*, *reduced lung volumes*, *irregular bronchial dilatation*, *traction bronchiectasis*, *normal DLCO*). Strip all conversational throat-clearing preamble (*"A 62-year-old male presenting with..."*, *"On histological examination of..."*, *"A supportive laboratory finding reflecting..."*).
   * **Conversational Clinician Phrasing & Direct Context Anchors (AnKing Style) (Agent 2):**
     - Open directly with the disease entity or finding: `"In [Disease],..."` or `"[Finding] with [Feature] is caused by {{c1::...}}"`. No artificial prefix tags (e.g. avoid `HRCT:`) unless the modality is strictly ambiguous, and zero fake patient vignettes (*"A 62yo man..."*).
     - Replace textbook jargon and passive multi-syllabic clauses with active, conversational clinical English (e.g. *"without needing PTH"* instead of *"develops independently of parathyroid hormone"*; *"make"* instead of *"autonomously express"*; *"tissue pulling and widening surrounding airways creates"* instead of *"caused by mechanical retractile forces exerted by surrounding contracted interstitial collagen"*; *"causes fibrotic nodules that classically favor"* instead of *"characteristically produces fibrotic nodules with a marked predilection for"*).
     - Conversational Brevity & Hard <= 20-Word Front Stem Linter: Optimize for conversational flow and shortness (target ~12–18 words per card). A build-time linter enforces a strict hard ceiling of <= 20 words per front stem, failing fast if any card exceeds 20 words to ensure a rapid 5–8 second reflex review speed.
   * **Strict 1–4 Word Cloze Ceiling & Fail-Fast Linter (Agent 2 & 3):** Cloze strictly the key entity, drug, parameter, or cutoff (1–4 words max). Never cloze full explanatory clauses or multi-word predicate phrases. A build-time linter automatically scans all clozes and fails fast if any cloze exceeds 4 words.
   * **Intelligent Semantic Coloring System (Vibrant Semantic Richness) (Agent 2 & 3):**
     - Front stems actively highlight **3–4+ distinct clinical entities** per card without adding filler text.
     - **5-Color Semantic Taxonomy:**
       1. Primary Concept / Subject / Disease Entity: `<u><b><span style="color:#00FF00;">...</span></b></u>` (Green `#00FF00`).
       2. Target Cloze Deletion (Anti-Spoiler Mandate): `<span style="color:#FFA500;"><b>{{cN::...}}</b></span>` (Orange `#FFA500`, span strictly OUTSIDE cloze brackets; blank NEVER adopts semantic colors).
       3. Clinical Signs, Symptoms, Microscopic Hallmarks & Pathologic Buzzwords: `<span style="color:#00FFFF;">...</span>` (Cyan `#00FFFF`, extracted directly from slide headers and audio cues like *"presents with"*, *"under microscope"*, *"gross appearance"*).
       4. Anatomic Site / Organ / Tissue Structure: `<span style="color:#FFB6C1;">...</span>` (Light Pink `#FFB6C1`).
       5. Key Demographic / Clinical Criterion / Cutoff / Lab Value: `<span style="color:#FFFF00;"><b>...</b></span>` (Yellow `#FFFF00`).
     - **AnKing Purple Harmony on Back Extra:** Strictly NO HTML color spans on the Back Extra (only standard `<b>`, `<i>`, and `<u>`).
     - **Automated Color Density Linter:** Build-time audit in `build_apkg.py` verifies presence of &ge; 2–3 distinct color spans per card and reports any sparse cards.
   * **Selective Professor Rationale Anchor (Agent 2):** When the professor provides an explicit verbal testing cue, exam warning, or board trap in the audio, open the Back Extra Rationale with the professor's formal name (e.g. *"<b>Rationale:</b> Dr. Zahidi explicitly emphasized this exam test: reversibility requires an FEV1 increase of &ge; 12% and &ge; 200 mL."*). Apply selectively (~25–40% of cards with spoken cues); never force it on routine definition cards.
   * **Explicit Branding:** Deck named `Medical School::[Discipline]::[Topic] [v2.1 LectureKing]`, file named `[Topic]_v2.1_LectureKing.apkg`.
   * Use when the user requests: **`run v2.1`**.

## Mandatory Version Clarification Rule
If the user asks to process a lecture or build a deck without specifying the version (e.g. *"process these slides and transcript to make .apkg"*), the agent **MUST explicitly ask**:
> *"Would you like to build this deck using **v2.1 (Recommended: Classmate-Refined & Transcript-Gated)**, **v2 (Original Natural Clinician)**, or **v1 (OG Exhaustive Architecture)**?"*

## Standard Execution Workflow
Regardless of version, the pipeline executes in 4 stages:
1. **OCR Extraction:** `fast_extract_ocr.py` extracts text from `<name> slides.pdf` into `slides_ocr_text.txt`.
2. **Agent 1 (Listener):** Analyzes transcript + slides OCR to create the High-Yield Blueprint.
3. **Agent 4 (Alignator):** Mapped blueprint with verified `[Slide_Number: XX]` tags.
4. **Agent 2 (Architect):** Drafts cloze flashcards following v1 or v2 specifications.
5. **Agent 3 (Formatter):** Formats cards into `<name>_anki_import_pipe.txt` with LectureKing semantic HTML colors and dynamic slide image tags `<img src="<prefix>_slide_XX.png">`.
6. **Packaging:** `build_apkg.py` renders all slides at 150 DPI and compiles `<Deck_Name>.apkg`.
