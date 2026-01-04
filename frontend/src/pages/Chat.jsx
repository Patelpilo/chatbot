import { useEffect, useRef, useState } from "react";
import { getChatHistory } from "../services/api";
import { connectSocket } from "../services/socket";

export default function Chat({ token, email, recipient }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [socketReady, setSocketReady] = useState(false);
  const socketRef = useRef(null);

  useEffect(() => {
    getChatHistory(token, recipient).then(setMessages);

    socketRef.current = connectSocket(token, (msg) => {
      setMessages((prev) => [...prev, msg]);
    });

    // set socketReady when connection opens
    if (socketRef.current) {
      socketRef.current.onopen = () => setSocketReady(true);
      socketRef.current.onclose = () => setSocketReady(false);
      socketRef.current.onerror = () => setSocketReady(false);
    }

    return () => socketRef.current && socketRef.current.close();
  }, [recipient]);

  function sendMessage() {
    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
      // avoid throwing when socket is not ready
      console.warn("WebSocket not ready - message not sent");
      return;
    }

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
