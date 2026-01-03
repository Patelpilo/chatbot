import { useState } from "react";
import { login, register } from "../services/api";

export default function Login({ onAuth }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleLogin() {
    const res = await login(email, password);
    if (res.access_token) {
      onAuth(res.access_token, email);
    } else {
      alert("Invalid credentials");
    }
  }

  async function handleRegister() {
    await register(email, password);
    alert("Registered successfully");
  }

  return (
    <div className="login">
      <h2>WhatsEase Login</h2>

      <input
        placeholder="Email"
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleLogin}>Login</button>
      <button onClick={handleRegister}>Register</button>
    </div>
  );
}
