import { useState, useRef, useEffect } from "react";
import axios from "axios";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/chat", {
        message: input,
      });

      const aiMessage = {
        role: "assistant",
        content: res.data.reply,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "❌ Backend error. Check FastAPI server.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <div className="flex flex-col w-full max-w-3xl mx-auto bg-white shadow-lg">
        
        {/* Header */}
        <div className="p-4 border-b text-center font-semibold text-lg">
          AI Chat (Groq)
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[75%] px-4 py-2 rounded-lg text-sm whitespace-pre-wrap
                ${
                  msg.role === "user"
                    ? "bg-black text-white rounded-br-none"
                    : "bg-gray-200 text-gray-900 rounded-bl-none"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="text-gray-400 italic text-sm">
              AI is thinking...
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="p-4 border-t flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
            placeholder="Type your message..."
            className="flex-1 resize-none border rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-black"
            rows={2}
          />
          <button
            onClick={sendMessage}
            disabled={loading}
            className="bg-black text-white px-5 rounded-lg hover:bg-gray-800 disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
