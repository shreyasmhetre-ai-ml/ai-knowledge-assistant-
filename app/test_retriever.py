from app.retriever import retrieve_chunks

query = "What is Python used for?"

chunks = retrieve_chunks(query)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}:")
    print(chunk)