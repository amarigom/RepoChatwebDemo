import React, { useState, useRef, useEffect } from "react";
import "./App.css";

export default function ChatApp() {
  const [sessionId, setSessionId] = useState(null);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  // Auto-scroll al final
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleUpload = async (e) => {
    const formData = new FormData();
    formData.append("file", e.target.files[0]);

    const res = await fetch("http://127.0.0.1:8000/upload_file/", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setSessionId(data.session_id);
  };

  const handleAsk = async () => {
    if (!sessionId || !question.trim()) return;

    const formData = new FormData();
    formData.append("session_id", sessionId);
    formData.append("question", question);

    const res = await fetch("http://127.0.0.1:8000/chat/", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setMessages((prev) => [...prev, { user: question, bot: data.answer }]);
    setQuestion("");
  };

  return (
    <div className="chat-container">
      <h1>Chat con PDF</h1>

      {!sessionId && (
        <div>
          <p>Subí un PDF/Excel/CSV para empezar:</p>
          <input type="file" accept="application/pdf" onChange={handleUpload} />
        </div>
      )}

      {sessionId && (
        <>
          <p className="session-info">Sesión activa: {sessionId}</p>

          <div className="chat-messages">
            {messages.map((m, i) => (
              <div key={i} className="message message-user">
                <p>{m.user}</p>
              </div>
            ))}
            {messages.map((m, i) => (
              <div key={i} className="message message-bot">
                <p>{m.bot}</p>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <div className="input-group">
            <input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Escribí tu pregunta..."
            />
            <button onClick={handleAsk}>Enviar</button>
          </div>
        </>
      )}
    </div>
  );
}
