from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil
import uuid

from app.database import create_table
from app.auth import register_user, login_user
from app.memory import add_message, get_messages
from app.pdf_processor import extract_text_from_pdf
from app.rag import ask_question
from app.text_chunker import split_text
from app.embedding import create_embedding
from app.vector_store import add_document


app = FastAPI()


create_table()


app.mount(
    "/frontend",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)


class ChatRequest(BaseModel):
    message: str
    session_id: str


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/")
def home():
    return {
        "message": "AI Knowledge Assistant is running"
    }


@app.post("/register")
def register(request: RegisterRequest):

    result = register_user(
        request.username,
        request.password
    )

    return result


@app.post("/login")
def login(request: LoginRequest):

    result = login_user(
        request.username,
        request.password
    )

    return result


@app.post("/chat")
def chat(request: ChatRequest):

    add_message(
        request.session_id,
        "user",
        request.message
    )

    response = ask_question(
        request.message,
        request.session_id
    )

    add_message(
        request.session_id,
        "assistant",
        response
    )

    return {
        "user_message": request.message,
        "bot_response": response
    }


@app.get("/chat-history/{session_id}")
def chat_history(session_id: str):

    messages = get_messages(session_id)

    return {
        "session_id": session_id,
        "messages": messages
    }


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = f"app/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)

    chunks = split_text(text)

    for i, chunk in enumerate(chunks):

        embedding = create_embedding(chunk)

        doc_id = (
            f"{file.filename}_"
            f"{i}_"
            f"{uuid.uuid4().hex}"
        )

        add_document(
            document=chunk,
            embedding=embedding,
            doc_id=doc_id
        )

    return {
        "filename": file.filename,
        "number_of_chunks": len(chunks),
        "message": "PDF processed and stored successfully!"
    }