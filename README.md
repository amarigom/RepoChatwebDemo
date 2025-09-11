Chat Web Demo

Demo de aplicación web que permite subir archivos (PDF, CSV, Excel) y hacer consultas tipo chat sobre su contenido, utilizando FastAPI, React y Gemini AI.

🚀 Funcionalidades

Subida de archivos PDF, CSV y Excel con múltiples hojas

Extracción de texto de los archivos para análisis

Chat interactivo para consultar información contenida en los archivos

Gestión de sesiones para mantener distintos contextos de archivos

Interfaz web construida en React

🧰 Herramientas utilizadas

Backend: Python, FastAPI, Uvicorn

Frontend: React, React DOM

Contenedores: Docker

Gestión de proyectos: Git, GitHub

🧩 Librerías utilizadas

Python / Backend

fastapi → Servidor y endpoints

uvicorn → Servidor ASGI

pandas → Manejo de datos CSV/Excel

PyPDF2 → Lectura de PDFs

python-dotenv → Variables de entorno .env

google-generativeai → Conexión con Gemini AI

Frontend / React

react, react-dom → Construcción de la interfaz

@testing-library/react, jest-dom → Tests de componentes

Testing / QA

Se puede usar Postman para probar los endpoints /upload_file/ y /chat/

Tests unitarios de React con Jest y Testing Library

🐳 Docker

La aplicación se puede ejecutar dentro de un contenedor Docker para facilitar el despliegue

Contiene un Dockerfile listo para construir la imagen y levantar el contenedor

Para ejecutar:

docker build -t chat-web-demo .
docker run -p 8000:8000 --env-file .env chat-web-demo

🔑 Variables de entorno

El archivo .env debe contener tu API Key de Gemini AI:

GOOGLE_API_KEY=TU_API_KEY


No compartas tu API Key en público. Cada usuario debe colocar la suya en su .env.

📌 Cómo usar

Clonar el repositorio

Crear un archivo .env con tu API Key

Ejecutar la aplicación con Docker o en local con Python (uvicorn main:app --reload)

Abrir el frontend en el navegador para interactuar con el chat

Subir archivos PDF, CSV o Excel y hacer preguntas sobre su contenido