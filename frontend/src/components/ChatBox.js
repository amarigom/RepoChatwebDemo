import React, { useState } from "react";

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(""); // Aquí va el session_id del PDF

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages([...messages, userMsg]);

    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, question: input })
      });
      const data = await res.json();

      const botMsg = { sender: "bot", text: data.answer || "No hay respuesta" };
      setMessages(prev => [...prev, userMsg, botMsg]);
    } catch (err) {
      console.error(err);
      const errorMsg = { sender: "bot", text: "Error de conexión con el backend" };
      setMessages(prev => [...prev, userMsg, errorMsg]);
    }

    setInput("");
  };

  return (
    <div>
      <div style={{ border: "1px solid #ccc", padding: 10, minHeight: 300, overflowY: "auto" }}>
        {messages.map((m, i) => (
          <div key={i} style={{ textAlign: m.sender === "user" ? "right" : "left" }}>
            <b>{m.sender}:</b> {m.text}
          </div>
        ))}
      </div>

      <input
        style={{ width: "80%", padding: 5, marginTop: 10 }}
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleSend()}
        placeholder="Escribí tu pregunta..."
      />
      <button style={{ width: "18%", padding: 5, marginLeft: "2%" }} onClick={handleSend}>
        Enviar
      </button>
    </div>
  );
}

export default ChatBox;
