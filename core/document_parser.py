"""Document parser for extracting text from various file formats."""

import io
import docx
import pdfplumber


def extract_text_from_file(uploaded_file) -> tuple[str, str, int, int]:
    """
    Extract text from uploaded file (PDF, DOCX, TXT).

    Returns:
        tuple: (text, filename, word_count, reading_time_minutes)
    """
    filename = uploaded_file.name
    file_extension = filename.split('.')[-1].lower()

    if file_extension == 'pdf':
        text = extract_pdf(uploaded_file)
    elif file_extension == 'docx':
        text = extract_docx(uploaded_file)
    elif file_extension == 'txt':
        text = uploaded_file.read().decode('utf-8')
    else:
        text = uploaded_file.read().decode('utf-8')

    word_count = len(text.split())
    reading_time = max(1, word_count // 200)

    return text, filename, word_count, reading_time


def extract_pdf(uploaded_file) -> str:
    """Extract text from PDF using pdfplumber."""
    text_parts = []

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

    return '\n\n'.join(text_parts)


def extract_docx(uploaded_file) -> str:
    """Extract text from DOCX using python-docx."""
    doc = docx.Document(uploaded_file)
    text_parts = []

    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text_parts.append(paragraph.text)

    return '\n\n'.join(text_parts)


def extract_text_from_textarea(text: str) -> tuple[str, str, int, int]:
    """Process raw text input."""
    word_count = len(text.split())
    reading_time = max(1, word_count // 200)
    return text, "Pasted Text", word_count, reading_time