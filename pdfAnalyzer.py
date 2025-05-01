import PyPDF2
import os
print(os.path.exists("Downloads\caitan.pdf"))

with open("Downloads\caitan.pdf", "rb") as f:
    reader = PyPDF2.PdfReader(f)
    page = reader.pages[0]  # First page
    media_box = page.mediabox
    width = float(media_box.width)
    height = float(media_box.height)
    print(f"Width: {width} pts, Height: {height} pts")