# LectureKing Flashcard Pipeline Specification: v1 vs. v2 vs. v2.1

This document defines the three parallel architectures available in this workspace. Any Antigravity agent session operating in `c:\Users\musta\OneDrive\Desktop\anki system` must adhere to these specifications.

---

## 1. Version Selection & Invocation Rules

* **Strict Explicit Version Required:**
  * When the user requests a deck with **`run v1`** (or *"run OG"*, *"use classic architecture"*), execute the **v1 (OG Architecture)** pipeline.
  * When the user requests a deck with **`run v2`** (or *"run v2 architecture"*), execute the **v2 (Natural Clinician / Student-Tested Tone)** pipeline.
  * When the user requests a deck with **`run v2.1`** (or *"run v2.1 architecture"*), execute the **v2.1 (Transcript-Gated & Classmate-Refined)** pipeline.
  * **If unspecified:** (e.g., the user only says *"process these slides and transcript to make .apkg"*), the agent **must ask for clarification**:
    > *"Would you like to build this deck using **v2.1 (Recommended: Classmate-Refined & Transcript-Gated)**, **v2 (Original Natural Clinician)**, or **v1 (OG Exhaustive Architecture)**?"*

---

## 2. Architecture Comparison Matrix

| Dimension | v1 (OG / Classic Architecture) | v2 (Natural Clinician Baseline) | v2.1 (Classmate-Refined & Transcript-Gated) |
| :--- | :--- | :--- | :--- |
| **Primary Goal** | Exhaustive reference; covers every slide detail | In-house exam mastery; high speed & low review fatigue | In-house exam mastery; zero 3rd-party bloat; strict lecture fidelity |
| **Primary Source** | Equal weight to Slides and Transcript | Transcript is primary clinical truth; slides provide context | **Transcript is strict gatekeeper**; slides provide structure & context |
| **Density Policy** | High density (~2.5–4 cards/min) | Organic density driven by clinical pivots (~1.2–2.2 cards/min) | **Pruned organic density**: Drops skipped slide bullets (~1.0–1.8 cards/min) |
| **Skipped Slide Bullets** | Creates cards for all bullets using external facts | May create cards if prominent on slide | **DROPPED entirely** (unless professor explicitly endorses the slide/table) |
| **Front Scope** | In-depth definitions & pathophysiology | Student-tested plain English | **Strict Slide-Transcript Boundary**: Front tests ONLY slide relationship |
| **Back Extra Context** | Deep mechanistic paragraphs | 2-part (`Rationale` + `Differentiator`) | **1-Sentence Definition in Rationale** for undefined slide terms |
| **Cloze Topology** | ~85–90% Single-Cloze (`c1` default) | Natural Dyad Standard (`c1` default; `c1`/`c2` twins) | **Natural Dyad Standard** (`c1` default; `c1`/`c2` twins; hard max `c2`, zero `c3`) |
| **Review Speed** | ~15–25 seconds per card | 6–8 seconds per card | **5–7 seconds per card** (fast reflex testing, zero clutter) |
| **Color Mandate** | Strict minimum 3–4 colors (padded) | Opportunistic 5-color (no padding) | **Vibrant Semantic Richness (3–4+ colored entities, anti-spoiler orange cloze, purple harmony back)** |
| **Deck Branding** | `[Topic]` | `[Topic] [v2 LectureKing]` | `[Topic] [v2.1 LectureKing]` |
| **Package File** | `[Topic].apkg` | `[Topic]_v2_LectureKing.apkg` | `[Topic]_v2.1_LectureKing.apkg` |

---

## 3. v1 Pipeline Specifications (OG / Frozen)

### Agent 1 (Listener — v1)
* Extract concept items covering every slide in chronological order.
* Assign 2 to 3 atomic cards per concept item.
* Treat slides and transcripts equally.

### Agent 4 (Alignator — v1)
* Map 100% of concept items to verified `[Slide_Number: XX]` tags.

### Agent 2 (Architect — v1)
* **Single-Cloze Preference (`c1` default):** ~85–90% of deck must be single `c1` cards.
* Split twin concepts (e.g. definition vs. mechanism) into separate cards.
* Strict 1–4 words per cloze.
* Formal academic phrasing.
* Back Extra: 2-part (`<b>Rationale:</b> ... <br><br><b>Differentiator:</b> ...`).

### Agent 3 (Formatter — v1)
* Pipe delimiter (` | `), 1 card per physical line.
* **Mandatory Color Quota:** Front text sentences must apply at least 3 to 4 distinct LectureKing colors (Green, Orange, Cyan, Pink, Yellow).
* Dynamic slide image embed: `<br><br><div class="slide-img-container"><img src="<prefix>_slide_XX.png"></div>`.

---

## 4. v2 Pipeline Specifications (Natural Clinician & Student Tone)

### Agent 1 (Listener — v2)
* **Transcript-First Clinical Cues:** Focus heavily on the professor's spoken emphasis, board traps, clinical vignettes, and testing cues. Slides provide anatomic and structural context.
* **Clinical Pivot & Anchor Rule:**
  * Include every actionable threshold (e.g. `RR > 60`, `Glucose ≤ 40 mg/dL`, `I:T > 0.20`, `PROM > 18h`).
  * Include normal baseline ranges *only* when anchored directly alongside their pathological counterpart in a comparative dyad.
  * Prune isolated non-actionable trivia that never acts as a decision point.
* **No Artificial Hard Caps:** Let the actual testable substance dictate the blueprint.

### Agent 4 (Alignator — v2)
* Map every concept item to its verified `[Slide_Number: XX]` tag chronologically.

### Agent 2 (Architect — v2)
* **Cloze Topology — Natural Dyad Standard:**
  * Default to single-cloze (`c1`) for standalone facts, mechanisms, and clinical pearls.
  * Systematically pair concepts into buryable **`c1`/`c2`** (hard max `c2`, zero `c3`) strictly for:
    1. *Normal Baseline vs. Pathological Cutoff* (e.g. resting RR `30–60` vs. tachypnea `> 60`).
    2. *Clinical Indication vs. Lethal Contraindication* (e.g. CDH: `immediate intubation` vs. `BVM contraindicated`).
    3. *Reciprocal Physiological Switches* (e.g. in utero `active chloride secretion` vs. labor `active sodium reabsorption via ENaC`).
    4. *Inseparable Twin Entities* (e.g. `Bochdalek` left-sided vs. `Morgagni` retrosternal; `GBS` term vs. `E. coli` preterm).
* **Student-Tested Phrasing (Zero Journal Fluff):**
  * Write in direct, plain clinical English the way a top medical student writes flashcards for peers.
  * Strip out multi-syllabic academic padding (e.g. write *"distends herniated bowel"* instead of *"due to lethal visceral distension"*).
  * Fast reflex testing: each card must be readable and answerable in 6–8 seconds.
* **Strict 1–4 Words per Cloze:** Key entities, cutoffs, medications, and terms only.
* **Back Extra:** 2-part (`<b>Rationale:</b>` 1–2 sentences + `<br><br>` + `<b>Differentiator:</b>` 1 comparative sentence).

### Agent 3 (Formatter — v2)
* Pipe delimiter (` | `), 1 card per physical line.
* **Opportunistic Color Palette:**
  * Primary Concept / Subject: `<u><b><span style="color:#00FF00;">Text</span></b></u>` (Green)
  * Target Term / Cloze Deletion: `<span style="color:#FFA500;"><b>{{cN::Text}}</b></span>` (Orange, span strictly outside cloze)
  * Mechanism / Action: `<span style="color:#00FFFF;">Text</span>` (Cyan)
  * Anatomic Site / Organ: `<span style="color:#FFB6C1;">Text</span>` (Light Pink)
  * Key Demographic / Cutoff: `<span style="color:#FFFF00;"><b>Text</b></span>` (Yellow)
  * **CRITICAL RULE:** Apply colors naturally to existing clinical terms. **NEVER** add words or stretch sentences to meet a color quota. A punchy 10-word card with 2 colors is vastly preferred over a bloated card with 5 colors.
* Dynamic slide image embed: `<br><br><div class="slide-img-container"><img src="<prefix>_slide_XX.png"></div>`.
* Clean HTML entities (`&gt;`, `&lt;`, `&ge;`, `&le;`), zero raw LaTeX.

---

## 5. v2.1 Pipeline Specifications (Transcript-Gated & Classmate-Refined Architecture)

### Agent 1 (Listener — v2.1)
* **The Transcript is the Strict Gatekeeper:** The lecture audio determines testability on the in-house exam.
* **The Skipped-Bullet Pruning Rule:** If a bullet point or named entity appears on a slide, but the professor spends 0 seconds on it in the audio (skips it or fails to mention it), DROP IT entirely. Do NOT invent cards for unmentioned slide trivia (AnKing/third-party decks already cover general Step 1 material).
* **The Endorsement Exception:** If the professor verbally points to a slide, diagram, or table and explicitly endorses it (*"make sure you know this table"*, *"this will be on the exam"*, *"pay attention to these criteria"*), all items in that endorsed table/slide are fair game even if the professor did not read every bullet aloud.
* **Clinical Pivot & Anchor Rule:** Every included item must center on an actionable diagnostic threshold, clinical cutoff, physiological switch, or clinical trap.

### Agent 4 (Alignator — v2.1)
* Map 100% of concept items to verified `[Slide_Number: XX]` tags chronologically.

### Agent 2 (Architect — v2.1)
* **The AnKing Gold Standard: Vignette-to-Punchline Clozing (~85–90% Single `c1`):**
  * Front stems must be structured like mini clinical vignettes: pack the patient demographic, geographic clue, environmental exposure, and associated symptoms into the un-clozed prompt stem.
  * Cloze ONLY the high-yield clinical punchline (the organism, first-line medication, unique histological hallmark, or actionable cutoff).
  * *BAD (Artificial Dyad - 2 cards to review!):* `"Histoplasma is endemic to {{c1::Ohio and Mississippi}} River Valleys and is transmitted via {{c2::bird or bat droppings}}."`
  * *BAD (Trivial Splitting - 2 cards to review!):* Card 1: `"Histoplasma is found in the {{c1::Ohio and Mississippi}} valleys."` Card 2: `"Histoplasma comes from {{c1::bird or bat}} droppings."` (Bloats deck with low-yield trivia recall).
  * *GOOD (AnKing Vignette-to-Punchline - 1 lean card!):* `"In a patient presenting with cavitary pulmonary lesions following cave exploration in the Ohio and Mississippi River Valleys, the primary suspected organism is {{c1::Histoplasma capsulatum}}."`
* **Standalone Secondary Pearls (Transcript-Driven):**
  * If the professor explicitly spends lecture time emphasizing a distinct clinical pivot (e.g. initial induction drug of choice, fastest diagnostic test, or pathognomonic biopsy feature), create a dedicated single `c1` card anchored by the clinical scenario:
  * *Example:* `"In a patient with severe disseminated histoplasmosis, the initial induction antifungal therapy of choice is {{c1::amphotericin B}}."`
  * NEVER combine the vignette setup and the medication into a lazy `c1`/`c2` pair like `"{{c1::severe histoplasmosis}} is treated with {{c2::amphotericin B}}"`.
* **Strict 10–15% Ceiling on `c1`/`c2` Dyads (Indivisible Dualities Only):**
  * Reserve `{{c1::...}}` and `{{c2::...}}` STRICTLY for true indivisible dualities where learning the reciprocal contrast is vital:
    1. *Reciprocal Thermal Dimorphism:* 25°C {{c1::mold / hyphae}} vs 37°C {{c2::yeast}}.
    2. *Head-to-Head Comparative Morphology:* Aspergillus {{c1::45° acute-angle septate hyphae}} vs Mucorales {{c2::90° right-angle non-septate hyphae}}.
    3. *Opposing Clinical Actions / Countermeasures:* CDH requires {{c1::immediate endotracheal intubation}} vs {{c2::bag-valve-mask (BVM) ventilation}} is strictly contraindicated.
  * If two facts describe the same disease entity (e.g. location, risk factor, symptom, drug), they are NOT a duality. Combine them into a single `c1` vignette card or grant the second fact its own dedicated `c1` card if endorsed by the professor.
  * **Hard Max `c2`, Zero `c3`**: Strictly zero `c3` clozes.
* **Strict Slide-Transcript Boundary on Fronts:**
  * Front stems test ONLY the direct relationship established on the slide or in the audio (e.g. *"Coal worker's pneumoconiosis carries a high risk of developing {{c1::Caplan syndrome}}"*).
  * **NEVER** import outside textbook definitions or deep external pathophysiology onto the Front (e.g. do NOT invent *"The development of multiple peripheral rheumatoid nodules in a patient with pneumoconiosis is known as..."* when the lecture only listed the syndrome name).
* **The Medical Noun Anchor Rule (SuperMemo Rules 10 & 12):**
  * Never prune key medical nouns, specific cell types, diagnostic parameters, exposures, or dual lab markers (e.g. keep *epithelioid macrophages*, *crystalline silica*, *hypercalciuria*, *reduced lung volumes*, *irregular bronchial dilatation*, *traction bronchiectasis*, *normal DLCO*).
  * Strip all conversational throat-clearing preamble (*"A 62-year-old male presenting with..."*, *"On histological examination of..."*, *"A supportive laboratory finding reflecting..."*).
* **Conversational Clinician Phrasing & Direct Context Anchors (AnKing Writing Style):**
  * Open directly with the disease entity or finding: `"In [Disease],..."` or `"[Finding] with [Feature] is caused by {{c1::...}}"`. No artificial prefix tags (e.g. avoid `HRCT:`) unless the modality is strictly ambiguous, and zero fake patient vignettes (*"A 62yo man..."*).
  * Replace textbook jargon and passive multi-syllabic clauses with active, conversational clinical English (e.g. *"without needing PTH"* instead of *"develops independently of parathyroid hormone"*; *"make"* instead of *"autonomously express"*; *"tissue pulling and widening surrounding airways creates"* instead of *"caused by mechanical retractile forces exerted by surrounding contracted interstitial collagen"*; *"causes fibrotic nodules that classically favor"* instead of *"characteristically produces fibrotic nodules with a marked predilection for"*).
  * Conversational Brevity & Hard <= 20-Word Front Stem Linter: Optimize for conversational flow and shortness (target ~12–18 words per card). A build-time linter enforces a strict hard ceiling of <= 20 words per front stem, failing fast if any card exceeds 20 words to ensure a rapid 5–8 second reflex review speed.
* **1-Sentence Plain Definition in Back Extra Rationale:**
  * When a term or syndrome is named on a slide without in-depth lecture explanation, define it in a single, plain-English sentence in the first line of the Back Extra `<b>Rationale:</b>` (e.g. *"<b>Rationale:</b> Caplan syndrome is the combination of pneumoconiosis with rheumatoid arthritis pulmonary nodules.<br><br><b>Differentiator:</b> Felty syndrome is rheumatoid arthritis with neutropenia and splenomegaly (no pulmonary nodules)."*).
  * Provides instant context for curious students without cluttering the Front or inflating review time.
* **Strict 1–4 Word Cloze Ceiling (Minimum Information Principle):**
  * Cloze STRICTLY the key entity, drug, parameter, or cutoff (1–4 words max).
  * **NEVER** cloze entire explanatory clauses, predicate phrases, or sentences (e.g. do NOT write `{{c1::PaO2 is below 70 mmHg (or A-a gradient &ge; 35 mmHg)}}`).
  * Restructure prompts so that conditions, anatomy, and descriptors sit in the prompt stem, leaving ONLY the 1–4 word punchline in the cloze (e.g. `...adjunctive corticosteroids are indicated if room air PaO2 is &le; {{c1::70 mmHg}} (or A-a gradient &ge; {{c2::35 mmHg}})`).
* **Anti-Spoiler Parenthetical Rule:**
  * NEVER leave an un-clozed parenthetical definition adjacent to the cloze on the Front (e.g. do NOT write `{{c1::tachypnea}} (respiratory rate > 20 bpm)` which gives away the answer). Enclose official abbreviations inside the cloze brackets: `{{c1::functional residual capacity (FRC)}}`.
* **Selective Professor Rationale Anchor (Instructor Voice):**
  * When the professor provides an explicit verbal testing cue, exam warning, board trap, or rule of thumb in the transcript, open the Back Extra `<b>Rationale:</b>` with the professor's formal name as supplied by the user (e.g. *"<b>Rationale:</b> Dr. Zahidi explicitly emphasized this exam test: reversibility requires an FEV1 improvement of &ge; 12% and &ge; 200 mL."* or *"<b>Rationale:</b> Dr. Shah's classic pitfall: despite its species name 'capsulatum', Histoplasma completely lacks a capsule."*).
  * Apply selectively to roughly 25–40% of cards that correspond to direct verbal emphasis; do NOT force it onto routine textbook definitions. This provides immediate psychological trust and in-house exam alignment for medical students.
* **Student-Tested Reflex Speed:** Plain clinical English, active voice, 5–7 second rapid recall.
* **HTML Entity Sanitization:** Zero raw LaTeX (`$`, `\frac`). Clean HTML (`&gt;`, `&lt;`, `&ge;`, `&le;`).

### Agent 3 (Formatter — v2.1)
* Pipe delimiter (` | `), 1 card per physical line.
* **Intelligent Semantic Coloring System (Vibrant Semantic Richness):**
  * Front stems actively highlight **3–4+ distinct clinical entities** per card without adding filler text.
  * **5-Color Semantic Taxonomy:**
    1. Primary Concept / Subject / Disease Entity: `<u><b><span style="color:#00FF00;">...</span></b></u>` (Green `#00FF00`).
    2. Target Cloze Deletion (Anti-Spoiler Mandate): `<span style="color:#FFA500;"><b>{{cN::...}}</b></span>` (Orange `#FFA500`, span strictly OUTSIDE cloze brackets; blank NEVER adopts semantic colors).
    3. Clinical Signs, Symptoms, Microscopic Hallmarks & Pathologic Buzzwords: `<span style="color:#00FFFF;">...</span>` (Cyan `#00FFFF`, extracted directly from slide headers and audio cues like *"presents with"*, *"under microscope"*, *"gross appearance"*).
    4. Anatomic Site / Organ / Tissue Structure: `<span style="color:#FFB6C1;">...</span>` (Light Pink `#FFB6C1`).
    5. Key Demographic / Clinical Criterion / Cutoff / Lab Value: `<span style="color:#FFFF00;"><b>...</b></span>` (Yellow `#FFFF00`).
* Dynamic slide image embed: `<br><br><div class="slide-img-container"><img src="<prefix>_slide_XX.png"></div>`.
* Clean AnKing purple harmony on Back Extra (zero color spans).
* **Automated Build-Time Linters:**
  * **Cloze-Length Linter (Fail-Fast):** Scans all `{{cN::...}}` instances across the deck. If any cloze exceeds 4 words, compilation halts immediately with an audit report.
  * **Color Density Linter (Auto-Audit & Warning):** Scans front stems for &ge; 2–3 distinct color spans in addition to the cloze, alerting on any under-colored cards.

---

## 6. Packaging Engine (`build_apkg.py`)
All architectures (v1, v2, v2.1) use the standard PyMuPDF 150 DPI render engine and genanki packaging model:
* Renders PDF pages to `<prefix>_slide_XX.png` at 150 DPI.
* Assigns unique Model ID and Deck ID.
* Imports pipe file and bundles images into `<Deck_Name>.apkg`.
* **Deck Branding Conventions:**
  * v1: `Medical School::[Discipline]::[Topic]`
  * v2: `Medical School::[Discipline]::[Topic] [v2 LectureKing]`
  * v2.1: `Medical School::[Discipline]::[Topic] [v2.1 LectureKing]`
* **Package File Naming:**
  * v1: `<Topic>.apkg`
  * v2: `<Topic>_v2_LectureKing.apkg`
  * v2.1: `<Topic>_v2.1_LectureKing.apkg`
