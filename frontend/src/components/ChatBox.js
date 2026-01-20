"use client";
import { useState } from "react";
import ModelSelector from "./ModelSelector";

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [model, setModel] = useState("gpt-4");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    setLoading(true);
    const res = await fetch("http://localhost:8000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input, model })
    });

    const data = await res.json();
    setMessages([...messages, { user: input, bot: data.reply }]);
    setInput("");
    setLoading(false);
  };

  return (
    <div className="bg-white w-96 p-4 rounded shadow">
      <ModelSelector model={model} setModel={setModel} />

      <div className="h-64 overflow-y-auto my-3">
        {messages.map((m, i) => (
          <div key={i}>
            <p className="text-blue-600">You: {m.user}</p>
            <p className="text-green-600">AI: {m.bot}</p>
          </div>
        ))}
        {loading && <p className="italic">AI is thinking...</p>}
      </div>

      <input
        className="border w-full p-2"
        value={input}
        onChange={e => setInput(e.target.value)}
      />
      <button
        onClick={sendMessage}
        className="bg-black text-white w-full mt-2 p-2"
      >
        Send
      </button>
    </div>
  );
}
