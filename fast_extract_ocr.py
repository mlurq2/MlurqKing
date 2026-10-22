# -*- coding: utf-8 -*-
"""
LectureKing: Fast Slide Text Extraction Script
Extracts all text from lecture slides PDF page-by-page with clear slide headers.
"""

import sys
import os
from pathlib import Path

try:
    import pymupdf as fitz
except ImportError:
    import fitz

def extract_slides_text(pdf_path, output_txt_path="slides_ocr_text.txt"):
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print(f"ERROR: Slide PDF file not found at '{pdf_path}'.")
        print("Usage: python fast_extract_ocr.py [slides.pdf] [output_text.txt]")
        sys.exit(1)
        
    print(f"Opening slide deck: {pdf_path.name}")
    doc = fitz.open(str(pdf_path))
    total_slides = len(doc)
    print(f"Total slides found: {total_slides}")
    
    with open(output_txt_path, "w", encoding="utf-8") as f:
        for page_idx in range(total_slides):
            page = doc[page_idx]
            slide_num = page_idx + 1
            text = page.get_text("text").strip()
            
            f.write(f"=== SLIDE {slide_num:02d} ===\n")
            f.write(text if text else "[NO TEXT / IMAGE SLIDE]")
            f.write("\n\n")
            
    print(f"SUCCESS! Extracted {total_slides} slides to: {output_txt_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print("LectureKing: Fast Slide Text Extraction Script")
        print("Usage: python fast_extract_ocr.py [slides.pdf] [output_text.txt]")
        sys.exit(0)
    elif len(sys.argv) > 1:
        input_pdf = sys.argv[1]
    else:
        # Look for default slides.pdf or any .pdf in the current directory
        cwd = Path(".")
        candidates = list(cwd.glob("*slides*.pdf")) or list(cwd.glob("*.pdf"))
        if candidates:
            input_pdf = candidates[0].name
        else:
            input_pdf = "slides.pdf"
            
    output_txt = sys.argv[2] if len(sys.argv) > 2 else "slides_ocr_text.txt"
    extract_slides_text(input_pdf, output_txt)
