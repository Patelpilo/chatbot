export function connectSocket(token, onMessage) {
  const socket = new WebSocket(
    `ws://127.0.0.1:8000/ws/chat?token=${token}`
  );

  socket.onmessage = (e) => {
    onMessage(JSON.parse(e.data));
  };

  return socket;
}
