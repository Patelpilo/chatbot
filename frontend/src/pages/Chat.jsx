import { useEffect, useRef, useState } from "react";
import { getChatHistory } from "../services/api";
import { connectSocket } from "../services/socket";
import "../styles/chat.css";

export default function Chat({ token, email, recipient }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [socketReady, setSocketReady] = useState(false);
  const [botWaiting, setBotWaiting] = useState(false);
  const socketRef = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    let mounted = true;
    getChatHistory(token, recipient).then((res) => mounted && setMessages(res || []));

    if (socketRef.current) {
      socketRef.current.close();
    }

    socketRef.current = connectSocket(token, (msg) => {
      if (msg.sender === "whatease_bot") {
        setBotWaiting(false);
      }

      setMessages((prev) => {
        const last = prev[prev.length - 1];
        if (last && last.sender === msg.sender && last.content === msg.content) {
          return prev;
        }
        return [...prev, msg];
      });
    });

    if (socketRef.current) {
      socketRef.current.onopen = () => {
        console.info("WS open");
        setSocketReady(true);
      };
      socketRef.current.onclose = (e) => {
        console.warn("WS closed", e);
        setSocketReady(false);
        setTimeout(() => {
          if (!socketRef.current || socketRef.current.readyState === WebSocket.CLOSED) {
            console.info("Attempting WS reconnect");
            socketRef.current = connectSocket(token, (msg) => {
              if (msg.sender === "whatease_bot") {
                setBotWaiting(false);
              }
              setMessages((prev) => [...prev, msg]);
            });
            socketRef.current.onopen = () => setSocketReady(true);
            socketRef.current.onclose = () => setSocketReady(false);
            socketRef.current.onerror = () => setSocketReady(false);
          }
        }, 1000);
      };
      socketRef.current.onerror = (e) => {
        console.error("WS error", e);
        setSocketReady(false);
      };

      if (socketRef.current.readyState === WebSocket.OPEN) {
        setSocketReady(true);
      }
    }

    return () => {
      mounted = false;
      socketRef.current && socketRef.current.close();
    };
  }, [recipient, token]);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  function sendMessage() {
    const text = input.trim();
    if (!text) return;

    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
      console.warn("WebSocket not ready - message not sent");
      return;
    }

    const msgObj = { recipient, content: text };

    if (recipient === "whatease_bot") {
      setBotWaiting(true);
    }

    socketRef.current.send(JSON.stringify(msgObj));
    setInput("");
  }

  function onKeyDown(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="chat">
      <div className="chat-header">
        <strong>{recipient}</strong>
        <span className={`status ${socketReady ? "online" : "offline"}`}>
          {socketReady ? "Connected" : "Disconnected"}
        </span>
      </div>

      <div className="messages" aria-live="polite">
        {messages.map((m, i) => (
          <div key={i} className={m.sender === email ? "me" : "them"}>
            {m.sender !== email && <strong>{m.sender}: </strong>}
            {m.content}
          </div>
        ))}
        {botWaiting && <div className="typing">whatease_bot is typing...</div>}
        <div ref={messagesEndRef} />
      </div>

      <div className="composer">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder={socketReady ? "Type a message..." : "Connecting..."}
          disabled={!socketReady}
        />
        <button onClick={sendMessage} disabled={!socketReady || input.trim() === ""}>
          Send
        </button>
      </div>
    </div>
  );
}
