import React, { useState } from 'react';
import Chat from './Chat';
import StatusBar from './components/StatusBar';

const NeuroHUD = () => {
  const [status, setStatus] = useState('Disconnected');

  return (
    <div className="neurohud">
      <Chat onStatusChange={setStatus} />
      <StatusBar status={status} />
    </div>
  );
};

export default NeuroHUD;
