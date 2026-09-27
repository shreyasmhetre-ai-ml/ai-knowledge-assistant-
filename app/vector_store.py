import chromadb


client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="knowledge_base"
)


def add_document(document, embedding, doc_id):

    collection.add(
        ids=[doc_id],
        documents=[document],
        embeddings=[embedding]
    )


def search_documents(query_embedding, top_k=3):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    print("Vector database is ready!")
    print("Collection:", collection.name)