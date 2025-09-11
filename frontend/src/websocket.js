function getWebSocketUrl() {
  const envUrl = import.meta.env.VITE_WS_URL;
  if (envUrl) return envUrl;
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  return `${protocol}//${window.location.host}/api/chat/ws`;
}

export function createWebSocket({ onMessage, onOpen, onClose }) {
  const ws = new WebSocket(getWebSocketUrl());
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

export function sendMessage(ws, message, mode) {
  const payload = { message };
  if (mode) {
    payload.mode = mode;
  } else {
    const remote = localStorage.getItem('remote_inference') === 'true';
    payload.mode = remote ? 'remote' : 'local';
  }
  ws.send(JSON.stringify(payload));
}

export function apiFetch(url, options = {}) {
  const remote = localStorage.getItem('remote_inference') === 'true';
  const headers = {
    ...(options.headers || {}),
    'X-Mode': remote ? 'remote' : 'local',
  };
  return fetch(url, { ...options, headers });
}
