import React, { useState } from 'react';
import NeuroHUD from './NeuroHUD';
import SettingsPanel from './components/SettingsPanel';
import './styles.css';

function App() {
  const [showSettings, setShowSettings] = useState(false);

  return (
    <div className="app">
      <button className="settings-toggle" onClick={() => setShowSettings(true)}>
        Settings
      </button>
      <NeuroHUD />
      {showSettings && <SettingsPanel onClose={() => setShowSettings(false)} />}
    </div>
  );
}

export default App;
