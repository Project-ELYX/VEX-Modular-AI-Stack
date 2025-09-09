export function createWebSocket({ onMessage, onOpen, onClose }) {
  const ws = new WebSocket('ws://localhost:8000/api/chat/ws');
  if (onMessage) {
    ws.onmessage = (event) => onMessage(event.data);
  }
  if (onOpen) {
    ws.onopen = onOpen;
  }
  if (onClose) {
    ws.onclose = onClose;
  }
  return ws;
}
