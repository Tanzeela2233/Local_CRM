from pathlib import Path
from pypdf import PdfReader

def extract_text(uploaded_file):
    name = uploaded_file.name.lower()

    if name.endswith(".txt"):
        raw = uploaded_file.getvalue()
        return raw.decode("utf-8", errors="ignore")

    if name.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        pages = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return "\n".join(pages)

    raise ValueError("Only PDF and TXT files are supported.")
