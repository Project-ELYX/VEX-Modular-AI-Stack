import React, { useEffect, useState } from 'react';

const SettingsPanel = ({ onClose }) => {
  const [openrouterKey, setOpenrouterKey] = useState('');
  const [anthropicKey, setAnthropicKey] = useState('');
  const [remoteInference, setRemoteInference] = useState(false);

  useEffect(() => {
    setOpenrouterKey(localStorage.getItem('openrouter_api_key') || '');
    setAnthropicKey(localStorage.getItem('anthropic_api_key') || '');
    setRemoteInference(localStorage.getItem('remote_inference') === 'true');
    // Fetch current backend config
    fetch('/api/config', {
      headers: { 'X-Token': 'secret-token' },
    })
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (!data) return;
        if (data.openrouter_api_key) setOpenrouterKey(data.openrouter_api_key);
        if (data.anthropic_api_key) setAnthropicKey(data.anthropic_api_key);
        setRemoteInference(data.mode === 'remote');
      })
      .catch(() => {});
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

  const saveConfig = async () => {
    const payload = {
      openrouter_api_key: openrouterKey || null,
      anthropic_api_key: anthropicKey || null,
      mode: remoteInference ? 'remote' : 'local',
    };
    try {
      await fetch('/api/config', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Token': 'secret-token',
        },
        body: JSON.stringify(payload),
      });
    } catch (err) {
      console.error('Failed to save config', err);
    }
  };

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
      <div className="actions">
        <button onClick={saveConfig}>Save</button>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default SettingsPanel;

