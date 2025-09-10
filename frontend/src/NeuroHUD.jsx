import React, { useEffect, useState } from 'react';
import Chat from './Chat';
import LogPanel from './components/LogPanel';
import StatusBar from './components/StatusBar';
import { createSocket } from './websocket';

export default function NeuroHUD() {
  const [socket, setSocket] = useState(null);
  const [status, setStatus] = useState('disconnected');
  const [log, setLog] = useState([]);

  useEffect(() => {
    const ws = createSocket();
    setSocket(ws);

    ws.addEventListener('open', () => setStatus('connected'));
    ws.addEventListener('close', () => setStatus('disconnected'));
    ws.addEventListener('error', () => setStatus('error'));
    ws.addEventListener('message', (e) => {
      setLog((prev) => [...prev, { type: 'recv', message: e.data }]);
    });

    return () => ws.close();
  }, []);

  const sendMessage = (msg) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(msg);
      setLog((prev) => [...prev, { type: 'sent', message: msg }]);
    }
  };

  return (
    <div className="neurohud">
      <StatusBar status={status} />
      <Chat onSend={sendMessage} />
      <LogPanel log={log} />
    </div>
  );
}
