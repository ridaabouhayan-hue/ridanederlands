import fitz
import os

pdf_files = [
    "WW-kunnen.pdf",
    "WW-moeten.pdf",
    "WW-mogen.pdf",
    "WW-willen.pdf",
    "WW-zullen.pdf"
]

images_dir = "images"
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

for pdf in pdf_files:
    if os.path.exists(pdf):
        print(f"Processing {pdf}...")
        doc = fitz.open(pdf)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=150)
            base = os.path.splitext(pdf)[0]
            output = os.path.join(images_dir, f"{base}_{page_num}.png")
            pix.save(output)
            print(f"Saved {output}")
        doc.close()
    else:
        print(f"File not found: {pdf}")
