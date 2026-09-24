# MlurqKing: Intelligent AI Anki Deck Generator 👑

MlurqKing is an open-source, multi-agent AI pipeline designed to automatically convert medical school lecture slides and transcripts into highly-yield, informative, and color-coded Anki flashcards (`.apkg`).

It uses a 4-agent architecture to extract high-yield concepts, prevent "giveaway" autocomplete clozes, format them with strict semantic HTML color rules, and dynamically embed high-resolution slide images onto the back of the cards.

## Features
- **4-Agent Pipeline**: Specialized agents for listening (yield detection), alignment (slide mapping), architecture (card drafting), and formatting.
- **Anti-Giveaway Rules**: Strict protocols prevent the AI from creating trivial clozes (like splitting eponyms or leaving parenthetical acronyms exposed). 
- **Semantic Color Coding**: Applies 4-5 distinct HTML colors to front text for rapid cognitive parsing (Concept, Cloze, Mechanism, Anatomy, Criteria).
- **Automated Image Embedding**: Extracts slides directly from your PDF and injects them into the `Back Extra` field of the corresponding Anki cards.

## Installation (Mac & Windows)

### 1. Prerequisites
- **Python 3.9+** installed on your computer.
- **Anki** desktop application.
- An AI assistant capable of reading multiple files (e.g., Claude 3.5 Sonnet via Claude Projects, ChatGPT Plus, or Google Antigravity).

### 2. Setup
1. Clone this repository or download it as a `.zip` and extract it:
   - Click the green **Code** button at the top right -> **Download ZIP**.
2. Open your terminal (Mac) or command prompt/PowerShell (Windows) and navigate to the extracted folder.
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to Use the Pipeline

### Step 1: Prep Your Files
1. Place your lecture slides PDF in the folder (e.g., `slides.pdf`).
2. Place your lecture transcript in the folder (e.g., `transcript.txt`).
3. Open `fast_extract_ocr.py` in a text editor and update the `pdf_file` variable to match your PDF's name. Run the script:
   ```bash
   python fast_extract_ocr.py
   ```
   *(This extracts all the text from your slides into `slides_ocr_text.txt` so the AI can read it).*

### Step 2: Run the AI Agents
You can run this using any advanced LLM. Here is how to do it in **Claude** (highly recommended via Claude Projects):

1. **Create a Project**: Go to Claude and create a new Project.
2. **Upload Knowledge**: Upload the 4 agent markdown files from the `prompts/` folder into the "Project Knowledge" section.
3. **Start a Chat**: Upload your `transcript.txt` and `slides_ocr_text.txt` to the chat.
4. **Execute**: Ask Claude to run the 4 agents sequentially. 
   - *Prompt*: "Please act as Agent 1 (Listener) and generate the blueprint based on my transcript and slides."
   - Follow up with Agent 4 (Alignator), Agent 2 (Architect), and Agent 3 (Formatter).
5. **Save Output**: Copy the final pipe-separated output (`|`) from Agent 3 and save it as `import_pipe.txt` in your local folder.

### Step 3: Build the `.apkg` Deck
1. Open `build_apkg.py` in a text editor.
2. Update the variables at the top of the script:
   - `PDF_PATH`: Name of your slides PDF.
   - `IMPORT_FILE`: Name of your pipe text file (`import_pipe.txt`).
   - `OUTPUT_APKG`: Desired name for your output deck (e.g., `Cardio_Lecture.apkg`).
   - `deck` (lines ~89): Update the Deck ID (change 1 digit so it's unique) and the Deck Name.
3. Run the packaging script:
   ```bash
   python build_apkg.py
   ```
4. Double-click the resulting `.apkg` file to import it directly into Anki! All images and colors will be perfectly formatted.

## About the Prompts
- **Agent 1 (Listener)**: Detects explicit/implicit professor cues to establish card yield and density.
- **Agent 2 (Architect)**: Drafts single-cloze (`c1`) cards. Enforces strict anti-giveaway rules (e.g., clozing entire multi-word eponyms, moving parentheticals inside the cloze).
- **Agent 3 (Formatter)**: Applies the 4-color semantic HTML mandate and constructs the Anki import syntax.
- **Agent 4 (Alignator)**: Maps concepts to exact slide numbers with zero hallucinations.

---
*Built by a medical student, for medical students. Stop spending 4 hours making cards, and start studying.*
