import ollama


def create_embedding(text):
    response = ollama.embed(
        model="nomic-embed-text",
        input=text
    )

    return response["embeddings"][0]


if __name__ == "__main__":
    text = "AI Knowledge Assistant is a chatbot."

    embedding = create_embedding(text)

    print("Embedding created successfully!")
    print("Vector size:", len(embedding))
    print("First 5 values:", embedding[:5])