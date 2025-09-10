import React, { useEffect, useState } from 'react';

const SettingsPanel = ({ onClose }) => {
  const [openrouterKey, setOpenrouterKey] = useState('');
  const [anthropicKey, setAnthropicKey] = useState('');
  const [remoteInference, setRemoteInference] = useState(false);

  useEffect(() => {
    setOpenrouterKey(localStorage.getItem('openrouter_api_key') || '');
    setAnthropicKey(localStorage.getItem('anthropic_api_key') || '');
    setRemoteInference(localStorage.getItem('remote_inference') === 'true');
  }, []);

  useEffect(() => {
    localStorage.setItem('openrouter_api_key', openrouterKey);
  }, [openrouterKey]);

  useEffect(() => {
    localStorage.setItem('anthropic_api_key', anthropicKey);
  }, [anthropicKey]);

  useEffect(() => {
    localStorage.setItem('remote_inference', remoteInference);
  }, [remoteInference]);

  return (
    <div className="settings-panel">
      <h2>Settings</h2>
      <label>
        OpenRouter API Key
        <input
          type="text"
          value={openrouterKey}
          onChange={(e) => setOpenrouterKey(e.target.value)}
        />
      </label>
      <label>
        Anthropic API Key
        <input
          type="text"
          value={anthropicKey}
          onChange={(e) => setAnthropicKey(e.target.value)}
        />
      </label>
      <label>
        <input
          type="checkbox"
          checked={remoteInference}
          onChange={(e) => setRemoteInference(e.target.checked)}
        />
        Enable Remote Inference
      </label>
      <button onClick={onClose}>Close</button>
    </div>
  );
};

export default SettingsPanel;

