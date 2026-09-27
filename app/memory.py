memory = {}


def add_message(session_id, role, message):

    if session_id not in memory:
        memory[session_id] = []

    memory[session_id].append({
        "role": role,
        "message": message
    })


def get_messages(session_id):

    if session_id not in memory:
        return []

    return memory[session_id]


if __name__ == "__main__":

    add_message("test123", "user", "Hello")
    add_message("test123", "assistant", "Hi! How can I help you?")

    messages = get_messages("test123")

    print(messages)