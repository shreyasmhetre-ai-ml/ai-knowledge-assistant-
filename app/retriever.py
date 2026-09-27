from app.vector_store import search_documents
from app.embedding import create_embedding


def retrieve_chunks(query, top_k=3):

    query_embedding = create_embedding(query)

    print("Query dimension:", len(query_embedding))

    results = search_documents(
        query_embedding=query_embedding,
        top_k=top_k
    )

    return results["documents"][0]