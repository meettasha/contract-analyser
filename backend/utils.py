import fitz
import docx

def extract_text(file_path):

    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        text = ""

        for page in doc:
            text += page.get_text()

        return text

    elif file_path.endswith(".docx"):

        doc = docx.Document(file_path)

        return "\n".join([p.text for p in doc.paragraphs])