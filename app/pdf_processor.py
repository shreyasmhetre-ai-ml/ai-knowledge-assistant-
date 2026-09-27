from pypdf import PdfReader
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text

if __name__ == "__main__":
    text = extract_text_from_pdf("app/sample.pdf")
    print(text)
    