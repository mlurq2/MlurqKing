"""
Build Vasculitides Anki Deck (.apkg) with High-Res Slide Images
"""

import os
import sys
import fitz  # PyMuPDF
import genanki
from pathlib import Path

WORKSPACE = Path(r"c:\Users\musta\OneDrive\Desktop\anki system")
PDF_PATH = WORKSPACE / "antiarythymmics slides.pdf"
IMPORT_FILE = WORKSPACE / "antiarrhythmics_anki_import_pipe.txt"
OUTPUT_APKG = WORKSPACE / "Antiarrhythmics_LectureKing.apkg"

def extract_slide_images():
    print("Extracting high-resolution slide images from PDF...")
    doc = fitz.open(PDF_PATH)
    image_paths = []
    
    for i, page in enumerate(doc):
        page_num = i + 1
        pix = page.get_pixmap(dpi=150)  # High quality 150 DPI render
        img_name = f"antiarrhythmics_slide_{page_num:02d}.png"
        img_path = WORKSPACE / img_name
        pix.save(str(img_path))
        image_paths.append((img_name, img_path))
        
    print(f"Extracted {len(image_paths)} slide images successfully.")
    return image_paths

def build_apkg():
    # 1. Extract slide images
    slide_images = extract_slide_images()
    media_files = [str(path) for name, path in slide_images]
    
    # 2. Define Anki Cloze Model (MUST specify model_type=genanki.Model.CLOZE)
    MODEL_ID = 1684920483
    DECK_ID = 2058193044
    
    cloze_model = genanki.Model(
        MODEL_ID,
        'LectureKing Cloze Model',
        fields=[
            {'name': 'Text'},
            {'name': 'Back Extra'}
        ],
        templates=[
            {
                'name': 'LectureKing Cloze Card',
                'qfmt': '{{cloze:Text}}',
                'afmt': '{{cloze:Text}}<br><hr id="answer"><div class="back-extra">{{Back Extra}}</div>',
            },
        ],
        css="""
        .card {
            font-family: Arial, Helvetica, sans-serif;
            font-size: 19px;
            text-align: left;
            color: #E2E8F0;
            background-color: #0F172A;
            padding: 20px;
            line-height: 1.5;
        }
        .cloze {
            font-weight: bold;
            color: #FFA500;
        }
        .back-extra {
            margin-top: 15px;
            font-size: 17px;
            color: #CBD5E1;
        }
        .slide-img-container {
            margin-top: 20px;
            text-align: center;
        }
        .slide-img-container img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            border: 2px solid #334155;
        }
        """,
        model_type=genanki.Model.CLOZE
    )

    deck = genanki.Deck(
        2058193065,
        'Medical School::Cardiology::Antiarrhythmics [LectureKing]'
    )

    # 3. Read cards from text file (supporting both | and ; delimiters)
    with open(IMPORT_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    notes_added = 0
    print(f"Processing {len(lines)} lines into Anki Deck...")
    for line in lines:
        if '|' in line:
            parts = line.split('|', 1)
        elif ';' in line:
            parts = line.split(';', 1)
        else:
            continue
            
        front_text = parts[0].strip()
        back_extra = parts[1].strip()
        
        note = genanki.Note(
            model=cloze_model,
            fields=[front_text, back_extra]
        )
        deck.add_note(note)
        notes_added += 1

    # 4. Package into .apkg
    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file(str(OUTPUT_APKG))
    print(f"SUCCESS! Added {notes_added} notes. Package created at: {OUTPUT_APKG}")

if __name__ == "__main__":
    build_apkg()
