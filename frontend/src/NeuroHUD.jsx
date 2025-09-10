import React from 'react';
import StatusBar from './components/StatusBar';

const NeuroHUD = ({ status }) => {
  return (
    <div className="neurohud">
      <StatusBar status={status} />
    </div>
  );
};

export default NeuroHUD;
