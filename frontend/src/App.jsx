import { useState } from "react";
import Login from "./pages/Login";
import Inbox from "./pages/Inbox";

export default function App() {
  const [token, setToken] = useState(null);
  const [email, setEmail] = useState(null);

  if (!token) {
    return (
      <Login
        onAuth={(t, e) => {
          setToken(t);
          setEmail(e);
        }}
      />
    );
  }

  return <Inbox token={token} email={email} />;
}
