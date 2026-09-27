from app.vector_store import add_document
from app.embedding import create_embedding
from app.text_chunker import split_text

text = """
Python is a programming language used for building applications,
web development, automation, data science and artificial intelligence.
"""

chunks = split_text(text)

for i, chunk in enumerate(chunks):
    embedding = create_embedding(chunk)

    add_document(
        document=chunk,
        embedding=embedding,
        doc_id=f"doc_{i}"
    )

print("Documents stored successfully!")