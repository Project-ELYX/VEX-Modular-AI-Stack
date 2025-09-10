export function createWebSocket({ onMessage, onOpen, onClose }) {
  const ws = new WebSocket('ws://localhost:8000/api/chat/ws');
  if (onMessage) {
    ws.onmessage = (event) => onMessage(JSON.parse(event.data));
  }
  if (onOpen) {
    ws.onopen = onOpen;
  }
  if (onClose) {
    ws.onclose = onClose;
  }
  return ws;
}

export function sendMessage(ws, message) {
  const remote = localStorage.getItem('remote_inference') === 'true';
  const payload = JSON.stringify({ message, mode: remote ? 'remote' : 'local' });
  ws.send(payload);
}

export function apiFetch(url, options = {}) {
  const remote = localStorage.getItem('remote_inference') === 'true';
  const headers = {
    ...(options.headers || {}),
    'X-Mode': remote ? 'remote' : 'local',
  };
  return fetch(url, { ...options, headers });
}
