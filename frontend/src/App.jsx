import React from 'react';
import ReactDOM from 'react-dom/client';
import NeuroHUD from './NeuroHUD';
import './styles.css';

function App() {
  return (
    <div className="app">
      <NeuroHUD />
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

export default App;
