const API_URL = "";

export async function login(email, password) {
  const res = await fetch("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return res.json();
}

export async function register(email, password) {
  return fetch("/auth/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
}

export async function getChatHistory(token, recipient) {
  const res = await fetch(`/chats/${recipient}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}
