# -*- coding: utf-8 -*-
"""
LectureKing v2.1 Anki Package Compiler (.apkg)
Features:
- High-Resolution 150 DPI Slide Extraction
- Automated Front Stem Word Count Linter (Fail-fast ceiling: <= 20 words, target 12-18)
- Automated Cloze Length Linter (Fail-fast ceiling: <= 4 words per cloze)
- Automated Semantic Color Density Linter (Audit for >= 3 distinct colors)
- Anti-Ugly LaTeX / Math Sanitizer (Converts raw $ to clean HTML)
- Native AnKing Dark-Mode CSS with Slide Image Embedding
"""

import os
import sys
import re
import argparse
import random
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:
    import fitz
import genanki

def extract_slide_images(pdf_paths, prefixes, output_dir, dpi=150):
    print("Checking / extracting high-resolution slide images from PDFs...")
    image_paths = []
    output_dir = Path(output_dir)
    
    for pdf_path, prefix in zip(pdf_paths, prefixes):
        pdf_file = Path(pdf_path)
        if not pdf_file.exists():
            print(f"ERROR: PDF file not found: {pdf_file}")
            sys.exit(1)
            
        doc = fitz.open(str(pdf_file))
        for i, page in enumerate(doc):
            page_num = i + 1
            img_name = f"{prefix}_slide_{page_num:02d}.png"
            img_path = output_dir / img_name
            if not img_path.exists():
                pix = page.get_pixmap(dpi=dpi)
                pix.save(str(img_path))
            image_paths.append((img_name, img_path))
            
    print(f"Verified {len(image_paths)} total slide images successfully.")
    return image_paths

def get_cloze_model():
    MODEL_ID = 1684920495
    return genanki.Model(
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

def audit_and_compile(pdf_paths, prefixes, import_file, deck_id, deck_name, output_apkg, dpi=150):
    print("\n" + "="*80)
    print(f"COMPILING DECK: {deck_name}")
    print(f"Import Source: {import_file}")
    print(f"Output Target: {output_apkg}")
    print("="*80)

    import_path = Path(import_file)
    if not import_path.exists():
        print(f"ERROR: Import file not found: {import_path}")
        sys.exit(1)

    # 1. Slide Images
    output_dir = import_path.parent
    slide_images = extract_slide_images(pdf_paths, prefixes, output_dir, dpi=dpi)
    media_files = [str(path) for name, path in slide_images]

    # 2. Cloze Model & Deck
    cloze_model = get_cloze_model()
    deck = genanki.Deck(deck_id, deck_name)

    # 3. Read cards
    with open(import_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # 3a. Cloze Length Linter (Max 4 words per cloze)
    cloze_violations = []
    for idx, line in enumerate(lines, 1):
        front = line.split('|', 1)[0].strip() if '|' in line else line.split(';', 1)[0].strip()
        clozes = re.findall(r'\{\{c\d+::(.*?)\}\}', front)
        for c in clozes:
            clean_text = re.sub(r'<[^>]+>', '', c).strip()
            clean_text = clean_text.replace('&alpha;', 'alpha').replace('&beta;', 'beta').replace('&gamma;', 'gamma').replace('&iuml;', 'i')
            words = clean_text.split()
            if len(words) > 4:
                cloze_violations.append((idx, len(words), clean_text))

    if cloze_violations:
        print("\n" + "="*80)
        print("BUILD HALTED: Strict 1-4 Word Cloze Violation Detected!")
        for line_no, word_count, text in cloze_violations:
            print(f"  * Line {line_no:02d} [{word_count} words]: \"{text}\"")
        print("="*80)
        sys.exit(1)

    # 3b. Front Stem Word Count Linter (Ceiling: Max 20 Words)
    stem_violations = []
    stem_word_counts = []
    for idx, line in enumerate(lines, 1):
        front = line.split('|', 1)[0].strip() if '|' in line else line.split(';', 1)[0].strip()
        clean_front = re.sub(r'<[^>]+>', '', front).strip()
        clean_front = clean_front.replace('&alpha;', 'alpha').replace('&beta;', 'beta').replace('&gamma;', 'gamma').replace('&iuml;', 'i')
        words = clean_front.split()
        stem_word_counts.append(len(words))
        if len(words) > 20:
            stem_violations.append((idx, len(words), clean_front))

    if stem_violations:
        print("\n" + "="*80)
        print("BUILD HALTED: Front Stem Word Count Violation Detected (> 20 words)!")
        print("Under LectureKing v2.1 AnKing reflex standard, front stems must be 12–18 words (max 20 words).")
        print(f"Found {len(stem_violations)} violating front stems:")
        print("="*80)
        for line_no, word_count, text in stem_violations:
            print(f"  * Line {line_no:02d} [{word_count} words]: \"{text}\"")
        print("="*80)
        sys.exit(1)

    avg_stem_words = sum(stem_word_counts) / len(stem_word_counts) if stem_word_counts else 0
    print(f"FRONT STEM WORD AUDIT: All {len(lines)} cards pass <= 20 words (Average: {avg_stem_words:.1f} words/card).")

    # 3c. Raw LaTeX Dollar Sign Sanitizer
    sanitized_lines = []
    for line in lines:
        if '$' in line:
            cleaned = re.sub(r'\$([^\$]+)\$', r'\1', line).replace('$', '')
            sanitized_lines.append(cleaned)
        else:
            sanitized_lines.append(line)
    lines = sanitized_lines

    # 3d. Color Density Linter
    color_palette = {
        'green': r'color:#00FF00',
        'orange': r'color:#FFA500',
        'cyan': r'color:#00FFFF',
        'pink': r'color:#FFB6C1',
        'yellow': r'color:#FFFF00'
    }
    
    color_audit = []
    sparse_cards = []
    for idx, line in enumerate(lines, 1):
        front = line.split('|', 1)[0].strip() if '|' in line else line.split(';', 1)[0].strip()
        found_colors = set()
        for c_name, c_hex in color_palette.items():
            if re.search(c_hex, front, re.IGNORECASE):
                found_colors.add(c_name)
        span_count = len(re.findall(r'<span style="color:[^"]+">', front))
        color_audit.append((idx, len(found_colors), span_count, found_colors))
        if len(found_colors) < 3:
            sparse_cards.append((idx, len(found_colors), span_count, found_colors, front))

    avg_colors = sum(c[1] for c in color_audit) / len(color_audit) if color_audit else 0
    print(f"COLOR DENSITY AUDIT: Average {avg_colors:.2f}/5 distinct colors per card.")
    if sparse_cards:
        print(f"WARNING: {len(sparse_cards)} cards have < 3 colors.")
    else:
        print("ALL CARDS MEET OR EXCEED >= 3 DISTINCT COLORS!")

    # 4. Add notes
    notes_added = 0
    for line in lines:
        parts = line.split('|', 1) if '|' in line else line.split(';', 1)
        front_text = parts[0].strip()
        back_extra = parts[1].strip()
        note = genanki.Note(model=cloze_model, fields=[front_text, back_extra])
        deck.add_note(note)
        notes_added += 1

    # 5. Write package
    output_path = Path(output_apkg)
    package = genanki.Package(deck)
    package.media_files = media_files
    package.write_to_file(str(output_path))
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\nSUCCESS! Added {notes_added} notes. Created: {output_path.name} ({file_size_mb:.2f} MB)")

def main():
    parser = argparse.ArgumentParser(description="LectureKing v2.1 Anki Package Compiler (.apkg)")
    parser.add_argument("--pdf", nargs="+", help="Path to one or more slide PDF files")
    parser.add_argument("--prefix", nargs="+", help="Prefix for slide images (e.g. 'lecture' for lecture_slide_01.png)")
    parser.add_argument("--pipe", default="import_pipe.txt", help="Path to pipe-separated card text file (default: import_pipe.txt)")
    parser.add_argument("--deck", default="Medical School::LectureKing Deck [v2.1 LectureKing]", help="Anki Deck Name")
    parser.add_argument("--deck-id", type=int, default=None, help="Unique Anki Deck ID (defaults to pseudo-random)")
    parser.add_argument("--output", default="Deck_v2.1_LectureKing.apkg", help="Output .apkg file path")
    parser.add_argument("--dpi", type=int, default=150, help="DPI for slide rendering (default: 150)")

    args = parser.parse_args()

    # If run with no CLI args, attempt to find sensible local defaults
    if not args.pdf:
        cwd = Path(".")
        candidates = list(cwd.glob("*slides*.pdf")) or list(cwd.glob("*.pdf"))
        if candidates:
            args.pdf = [candidates[0].name]
            print(f"Auto-detected slide PDF: {args.pdf[0]}")
        else:
            print("ERROR: No PDF specified and no PDF found in current folder.")
            print("Usage example:")
            print("  python build_apkg.py --pdf slides.pdf --pipe import_pipe.txt --deck \"Medical School::Pathology::Neoplasia [v2.1 LectureKing]\" --output Neoplasia_v2.1.apkg")
            sys.exit(1)

    if not args.prefix:
        args.prefix = [Path(p).stem.replace(" slides", "").replace(" ", "_").lower() for p in args.pdf]

    if args.deck_id is None:
        args.deck_id = random.randint(1000000000, 2099999999)

    audit_and_compile(
        pdf_paths=args.pdf,
        prefixes=args.prefix,
        import_file=args.pipe,
        deck_id=args.deck_id,
        deck_name=args.deck,
        output_apkg=args.output,
        dpi=args.dpi
    )

if __name__ == "__main__":
    main()
