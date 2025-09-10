import React from 'react';

export default function LogPanel({ log }) {
  return (
    <div className="log-panel">
      <h2>Log</h2>
      <ul>
        {log.map((entry, idx) => (
          <li key={idx}>
            <strong>{entry.type === 'sent' ? 'You' : 'Server'}:</strong> {entry.message}
          </li>
        ))}
      </ul>
    </div>
  );
}
