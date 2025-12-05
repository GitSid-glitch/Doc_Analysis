import pdfplumber
import docx

def extract_pdf_text(filepath):
    with pdfplumber.open(filepath) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def extract_docx_text(filepath):
    doc = docx.Document(filepath)
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return text
