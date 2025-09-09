import React from 'react';

const LogPanel = ({ messages }) => {
  return (
    <div className="log-panel">
      {messages.map((m, i) => (
        <div key={i} className={`message ${m.role}`}>
          {m.content}
        </div>
      ))}
    </div>
  );
};

export default LogPanel;
