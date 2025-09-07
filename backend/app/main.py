from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uuid
import PyPDF2

import google.generativeai as genai
import os

# 🔑 Configura tu API Key de Gemini
os.environ["GOOGLE_API_KEY"] = "AIzaSyCGziNtswrtn4x8ThttDZ-7voAYp0Kgqxw"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
print("API Key:", os.environ.get("GOOGLE_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción poné solo tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Guardamos las sesiones
sessions = {}

# Función para extraer texto del PDF
def extract_text_from_pdf(file) -> str:
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text


@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile):
    session_id = str(uuid.uuid4())
    
    # Extraer texto del PDF
    pdf_text = extract_text_from_pdf(file.file)
    
    # Guardamos el texto en la sesión
    sessions[session_id] = {"file": file.filename, "content": pdf_text}
    
    print(f"📂 PDF cargado en sesión {session_id}: {file.filename}")
    print(f"\n📂 PDF recibido: {file.filename} | Sesión: {session_id}")
    print(f"📄 Texto extraído (primeros 500 caracteres): {pdf_text[:500]}...\n")
    return {"session_id": session_id}


@app.post("/chat/")
async def chat(session_id: str = Form(...), question: str = Form(...)):
    if session_id not in sessions:
        return {"answer": "⚠️ Sesión no encontrada."}
    
    pdf_content = sessions[session_id]["content"]
    
    # Gemini recibe la pregunta + el contenido del PDF
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"El siguiente texto viene de un PDF:\n\n{pdf_content}\n\nPregunta: {question}"
    
    response = model.generate_content(prompt)
    print(f"\n👉 Pregunta: {question}\n🤖 Respuesta: {response}\n")
    return {"answer": response.text}
