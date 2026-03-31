#!/usr/bin/env python3
"""
Add a colored border frame to PDF files.
Uses reportlab to create a border overlay.
"""

import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor


def create_border_page(width, height, border_color="#4f46e5", border_width=1.5, margin=18):
    """Create a single page with border frame."""
    from io import BytesIO
    
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    
    # Convert margin from points (1 pt = 1/72 inch)
    m = margin
    
    # Draw border rectangle
    c.setStrokeColor(HexColor(border_color))
    c.setLineWidth(border_width)
    c.rect(m, m, width - 2*m, height - 2*m, fill=0, stroke=1)
    
    c.save()
    packet.seek(0)
    
    from pypdf import PdfReader
    return PdfReader(packet)


def add_border_to_pdf(input_path, output_path, border_color="#4f46e5", border_width=1.5):
    """Add border frame to all pages of a PDF."""
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        # Get page dimensions
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        
        # Create border page matching dimensions
        border_pdf = create_border_page(width, height, border_color, border_width)
        border_page = border_pdf.pages[0]
        
        # Merge border onto page
        page.merge_page(border_page)
        writer.add_page(page)
    
    with open(output_path, 'wb') as f:
        writer.write(f)
    
    print(f"✅ Added {border_color} border to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pdf_add_border.py <input.pdf> [output.pdf] [--color COLOR] [--width WIDTH]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else input_file
    
    # Parse optional args
    color = "#4f46e5"  # indigo default
    width = 1.5
    
    for i, arg in enumerate(sys.argv):
        if arg == "--color" and i + 1 < len(sys.argv):
            color = sys.argv[i + 1]
        if arg == "--width" and i + 1 < len(sys.argv):
            width = float(sys.argv[i + 1])
    
    add_border_to_pdf(input_file, output_file, color, width)
