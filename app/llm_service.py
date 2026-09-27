import ollama


def generate_response(history):
    response = ollama.chat(
        model="llama3.2",
        messages=history
    )

    return response.message.content