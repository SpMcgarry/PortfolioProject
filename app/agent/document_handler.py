import os
from docx import Document
from PyPDF2 import PdfReader
from agent.memory import add_memory

DOC_FOLDER = "documents"

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def scan_documents():
    for filename in os.listdir(DOC_FOLDER):
        path = os.path.join(DOC_FOLDER, filename)
        if filename.lower().endswith(".docx"):
            text = extract_text_from_docx(path)
        elif filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(path)
        else:
            continue
        add_memory({"type": "document", "filename": filename, "content": text})
