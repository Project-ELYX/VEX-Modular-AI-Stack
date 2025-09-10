import React, { useState } from 'react';
import Chat from './Chat';
import NeuroHUD from './NeuroHUD';
import SettingsPanel from './components/SettingsPanel';
import './styles.css';

function App() {
  const [showSettings, setShowSettings] = useState(false);
  const [status, setStatus] = useState('Disconnected');

  return (
    <div className="app">
      <button className="settings-toggle" onClick={() => setShowSettings(true)}>
        Settings
      </button>
      <Chat onStatusChange={setStatus} />
      <NeuroHUD status={status} />
      {showSettings && <SettingsPanel onClose={() => setShowSettings(false)} />}
    </div>
  );
}

export default App;
