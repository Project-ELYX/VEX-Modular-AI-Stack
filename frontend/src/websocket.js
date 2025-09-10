export const WS_URL = 'ws://localhost:8000/api/chat/ws';

export function createSocket() {
  return new WebSocket(WS_URL);
}
