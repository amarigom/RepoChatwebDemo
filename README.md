**Negrita** 
# Chat Web Demo

Aplicación web que permite subir archivos PDF, CSV o Excel, extraer su contenido y realizar consultas mediante un chat interactivo utilizando **Google Gemini AI**.

---

## 🚀 Características

- Subida de archivos: PDF, CSV, XLSX.  
- Extracción de texto de documentos y hojas de cálculo.  
- Chat interactivo que responde preguntas basadas en el contenido del archivo.  
- Sistema de sesiones único por usuario.  
- Compatible con **Postman** para pruebas del backend.  

---

## 🛠 Herramientas utilizadas

- **Frontend:** React  
- **Backend:** FastAPI  
- **Contenedores:** Docker  
- **Testing:** Postman, Jest  
- **IA:** Google Gemini API  

---

## 📚 Librerías principales

- `PyPDF2` → Para leer PDFs  
- `pandas` → Para manejar CSV y Excel  
- `openpyxl` → Motor de Excel para pandas  
- `python-dotenv` → Para cargar variables de entorno  
- `fastapi` → Framework web backend  
- `google-generativeai` → Integración con Gemini AI  
- `@testing-library/jest-dom` → Para tests en frontend React  

---

## ⚙️ Variables de entorno

GOOGLE_API_KEY=REEMPLAZAR_CON_TU_API_KEY
Nota: No compartas tu API Key públicamente. Se recomienda añadir .env al .gitignore.
---
## 🐳 Uso con Docker
- Construir imagen
docker build -t chat-web-demo-backend .

- Ejecutar contenedor
docker run -p 8000:8000 --env-file .env chat-web-demo-backend


Esto expondrá la API en http://localhost:8000

## 💻 Ejecución local sin Docker

- Crear un entorno virtual:

python -m venv venv


- Activar el entorno y instalar dependencias:

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt


- Ejecutar la app:

uvicorn main:app --reload

---
## 🧪 Pruebas con Postman

Endpoint para subir archivos: POST /upload_file/

Endpoint de chat: POST /chat/

Cada solicitud debe incluir el session_id obtenido al subir un archivo.

Se recomienda crear un Collection en Postman para agrupar todos los tests.
---
## 📂 Estructura del proyecto
chat-web-demo/
├─ backend/
│  ├─ main.py
│  ├─ requirements.txt
│  └─ .env (no subir a GitHub)
├─ frontend/
│  ├─ src/
│  ├─ package.json
│  └─ ... push
├─ Dockerfile
├─ docker-compose.yml (opcional)
└─ README.md
---
## ✅ Notas finales

- El proyecto está preparado para ser desplegado localmente o en contenedores Docker.

- Para ejecutar en otra máquina, basta con clonar el repo, instalar dependencias y configurar el .env con la API Key correspondiente.

- Se puede utilizar Postman para testear la API sin necesidad de frontend.