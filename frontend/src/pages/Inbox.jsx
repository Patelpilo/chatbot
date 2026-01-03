import { useState } from "react";
import Chat from "./Chat";

export default function Inbox({ token, email }) {
  const [activeChat, setActiveChat] = useState(null);

  return (
    <div className="inbox">
      <div className="sidebar">
        <h3>Chats</h3>
        <button onClick={() => setActiveChat("whatease_bot")}>
          🤖 WhatsEase Bot
        </button>
      </div>

      <div className="chat-area">
        {activeChat ? (
          <Chat token={token} email={email} recipient={activeChat} />
        ) : (
          <p>Select a chat</p>
        )}
      </div>
    </div>
  );
}
