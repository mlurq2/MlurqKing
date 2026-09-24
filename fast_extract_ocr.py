import fitz  # PyMuPDF
import sys
import os

def extract_slides_text(pdf_path, output_txt_path):
    print(f"Extracting text from: {pdf_path}")
    doc = fitz.open(pdf_path)
    print(f"Total slides: {len(doc)}")
    
    with open(output_txt_path, "w", encoding="utf-8") as f:
        for page_idx in range(len(doc)):
            page = doc[page_idx]
            slide_num = page_idx + 1
            text = page.get_text("text").strip()
            
            f.write(f"=== SLIDE {slide_num:02d} ===\n")
            f.write(text if text else "[NO TEXT / IMAGE SLIDE]")
            f.write("\n\n")
            
    print(f"SUCCESS! Slide OCR text saved to: {output_txt_path}")

if __name__ == "__main__":
    pdf_file = "antiarythymmics slides.pdf"
    output_file = "slides_ocr_text.txt"
    extract_slides_text(pdf_file, output_file)
