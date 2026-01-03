import { useEffect, useRef, useState } from "react";
import { getChatHistory } from "../services/api";
import { connectSocket } from "../services/socket";

export default function Chat({ token, email, recipient }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const socketRef = useRef(null);

  useEffect(() => {
    getChatHistory(token, recipient).then(setMessages);

    socketRef.current = connectSocket(token, (msg) => {
      setMessages((prev) => [...prev, msg]);
    });

    return () => socketRef.current.close();
  }, [recipient]);

  function sendMessage() {
    socketRef.current.send(
      JSON.stringify({ recipient, content: input })
    );
    setInput("");
  }

  return (
    <div className="chat">
      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={m.sender === email ? "me" : "them"}>
            {m.content}
          </div>
        ))}
      </div>

      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
