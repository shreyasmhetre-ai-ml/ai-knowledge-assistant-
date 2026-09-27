from app.retriever import retrieve_chunks
from app.memory import get_messages
import requests


def ask_question(question, session_id):

    # 1. Retrieve relevant document chunks
    chunks = retrieve_chunks(question)

    # 2. Combine document chunks
    context = "\n\n".join(chunks)

    # 3. Get previous conversation
    messages = get_messages(session_id)

    conversation = ""

    for message in messages:
        conversation += f"{message['role']}: {message['message']}\n"

    # 4. Create prompt
    prompt = f"""
You are an AI Knowledge Assistant.

Use the document context and previous conversation to answer the question.

Document Context:
{context}

Previous Conversation:
{conversation}

Current Question:
{question}

Answer:
"""

    # 5. Send prompt to Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    # 6. Return answer
    return response.json()["response"]


if __name__ == "__main__":

    question = "What is Python used for?"
    session_id = "test123"

    answer = ask_question(question, session_id)

    print("\nAnswer:")
    print(answer)