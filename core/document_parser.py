"""
UnderstandIQ Document Parser
Extracts clean text from PDF, DOCX, and raw text input.
"""

import io


def extract_text_from_file(uploaded_file):
    filename = uploaded_file.name
    ext = filename.lower().split(".")[-1]
    text = ""

    try:
        if ext == "pdf":
            import pdfplumber
            with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                pages = [p.extract_text() or "" for p in pdf.pages]
                text = "\n".join(pages)
        elif ext == "docx":
            from docx import Document
            doc = Document(io.BytesIO(uploaded_file.read()))
            text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        elif ext == "txt":
            text = uploaded_file.read().decode("utf-8", errors="ignore")
    except Exception as e:
        text = ""

    text = text.strip()
    word_count = len(text.split()) if text else 0
    reading_time = max(1, word_count // 200)
    return text, filename, word_count, reading_time


def extract_text_from_textarea(raw_text: str):
    text = raw_text.strip()
    word_count = len(text.split()) if text else 0
    reading_time = max(1, word_count // 200)
    return text, "Pasted Text", word_count, reading_time
