from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile):
    session_id = str(uuid.uuid4())
    # acá deberías procesar y guardar el PDF para esa sesión
    sessions[session_id] = {"file": file.filename}
    print("\n--- Estado actual de sessions ---")
    print(sessions)
    print("---------------------------------\n")
    
    return {"session_id": session_id}

@app.post("/chat/")
async def chat(session_id: str = Form(...), question: str = Form(...)):
    if session_id not in sessions:
        return {"answer": "Sesión no encontrada"}
    print(f"\n👉 Pregunta recibida en sesión {session_id}: {question}\n")
    print("Sessions actuales:", sessions)
    # acá deberías usar tu motor de QA con el PDF de la sesión
    return {"answer": f"Respuesta simulada a: '{question}' con el PDF {sessions[session_id]['file']}"}
