import React, { useEffect, useRef, useState } from 'react';
import LogPanel from './components/LogPanel';
import { createWebSocket, sendMessage } from './websocket';

const Chat = ({ onStatusChange }) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [stream, setStream] = useState('');
  const wsRef = useRef(null);

  useEffect(() => {
    wsRef.current = createWebSocket({
      onOpen: () => onStatusChange && onStatusChange('Connected'),
      onClose: () => onStatusChange && onStatusChange('Disconnected'),
      onMessage: (raw) => {
        let data;
        try {
          data = JSON.parse(raw);
        } catch {
          return;
        }
        if (data.token) {
          setStream((prev) => prev + data.token);
        }
        if (data.reply) {
          setMessages((prev) => [...prev, { role: 'assistant', content: data.reply }]);
          setStream('');
        }
      },
    });
    return () => wsRef.current && wsRef.current.close();
  }, [onStatusChange]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages((prev) => [...prev, { role: 'user', content: input }]);
    setStream('');
    if (wsRef.current) {
      sendMessage(wsRef.current, input);
    }
    setInput('');
  };

  const allMessages = stream
    ? [...messages, { role: 'assistant', content: stream }]
    : messages;

  return (
    <div className="chat">
      <LogPanel messages={allMessages} />
      <form onSubmit={handleSubmit} className="chat-input">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Say something"
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default Chat;
