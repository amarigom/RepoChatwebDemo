import React, { useState } from "react";
import axios from "axios";
import "./ChatApp.css"; // si ya tenés tu CSS

export default function ChatApp() {
  const [sessionId, setSessionId] = useState(null);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);

  // 👉 Subir PDF
  const handleUpload = async (e) => {
    try {
      const formData = new FormData();
      formData.append("file", e.target.files[0]);

      const res = await axios.post(
        "http://127.0.0.1:8000/upload_pdf/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      setSessionId(res.data.session_id);
      console.log("📂 PDF subido. Session ID:", res.data.session_id);
    } catch (err) {
      console.error("❌ Error al subir PDF:", err);
    }
  };

  // 👉 Hacer pregunta
  const handleAsk = async () => {
    if (!sessionId || !question.trim()) return;

    try {
      const formData = new FormData();
      formData.append("session_id", sessionId);
      formData.append("question", question);

      const res = await axios.post("http://127.0.0.1:8000/chat/", formData);

      setMessages((prev) => [...prev, { q: question, a: res.data.answer }]);
      setQuestion("");
    } catch (err) {
      console.error("Error en el chat:", err);
    }
  };

  return (
    <div className="chat-container">
      <h1 className="chat-title">Chat incorporando PDF</h1>

      {!sessionId && (
        <div className="upload-section">
          <p>Subí tu PDF para empezar:</p>
          <input type="file" accept="application/pdf" onChange={handleUpload} />
        </div>
      )}

      {sessionId && (
        <div className="chat-box">
          <p className="session-id">Sesión activa: {sessionId}</p>

          <div className="input-area">
            <input
              className="chat-input"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Escribí tu pregunta..."
            />
            <button onClick={handleAsk} className="chat-button">
              Preguntar
            </button>
          </div>

          <div className="messages">
            {messages.map((m, i) => (
              <div key={i} className="message">
                <p className="msg-user"> Tú: {m.q}</p>
                <p className="msg-bot"> Bot: {m.a}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
