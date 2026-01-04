export function connectSocket(token, onMessage) {
  // Use same-origin WebSocket URL so it works over HTTPS (wss) and through Vite proxy
  const proto = window.location.protocol === "https:" ? "wss" : "ws";
  const host = window.location.host;
  const url = `${proto}://${host}/ws/chat?token=${encodeURIComponent(token)}`;

  const socket = new WebSocket(url);

  socket.onopen = () => console.info("WS open", url);
  socket.onclose = (e) => console.warn("WS closed", e);
  socket.onerror = (e) => console.error("WS error", e);
  socket.onmessage = (e) => {
    try {
      onMessage(JSON.parse(e.data));
    } catch (err) {
      console.error("Failed parsing WS message", err, e.data);
    }
  };

  return socket;
}
