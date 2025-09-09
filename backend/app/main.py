from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os
import PyPDF2
import pandas as pd
import google.generativeai as genai

# 🔑 Configura tu API Key de Gemini
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")

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

# Función para extraer texto de PDF
def extract_text_from_pdf(file) -> str:
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Función para extraer texto de Excel o CSV
def extract_text_from_excel(file, filename) -> str:
    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        # Convertimos todo a texto: cada fila como línea y columnas separadas por '|'
        text = df.astype(str).apply(lambda row: " | ".join(row), axis=1).str.cat(sep="\n")
        return text
    except Exception as e:
        return f"⚠️ Error leyendo archivo: {e}"

# Endpoint unificado para subir cualquier archivo
@app.post("/upload_file/")
async def upload_file(file: UploadFile):
    import pandas as pd
    import io

    session_id = str(uuid.uuid4())
    filename = file.filename.lower()

    content = ""
    file_type = ""
    sheet_names = []  # solo para Excel

    if filename.endswith(".pdf"):
        # PDF
        content = extract_text_from_pdf(file.file)
        file_type = "pdf"

    elif filename.endswith(".csv"):
        # CSV
        df = pd.read_csv(io.StringIO(file.file.read().decode("utf-8")))
        content = df.to_string()
        file_type = "csv"

    elif filename.endswith(".xlsx"):
        # Excel con múltiples hojas
        xls = pd.read_excel(file.file, sheet_name=None, engine="openpyxl")
        content = ""
        for sheet, df in xls.items():
            sheet_names.append(sheet)
            content += f"\n\n--- 📑 Hoja: {sheet} ---\n"
            content += df.to_string()
        file_type = "xlsx"

    else:
        return {"error": "⚠️ Formato no soportado. Solo PDF, CSV o XLSX."}

    # Guardamos sesión con tipo y contenido
    sessions[session_id] = {
        "file": file.filename,
        "content": content,
        "type": file_type
    }

    print(f"📂 Archivo cargado en sesión {session_id}: {file.filename}")
    print(f"📄 Contenido extraído (primeros 500 caracteres): {content[:500]}...\n")

    return {
        "session_id": session_id,
        "file": file.filename,
        "type": file_type,
        "sheets": sheet_names if sheet_names else None
    }


# Endpoint unificado de chat
@app.post("/chat/")
async def chat(session_id: str = Form(...), question: str = Form(...)):
    if session_id not in sessions:
        return {"answer": "⚠️ Sesión no encontrada."}
    
    file_content = sessions[session_id]["content"]
    file_type = sessions[session_id]["type"]
    
    # Generamos el prompt para Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"El siguiente texto viene de un archivo {file_type}:\n\n{file_content}\n\nPregunta: {question}"
    
    response = model.generate_content(prompt)
    
    print(f"\n👉 Pregunta: {question}\n🤖 Respuesta: {response}\n")
    return {"answer": response.text}
