import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import authService from './Auth/Keyclock';
import './index.css';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

authService.init()
  .then(() => {
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
  })
  .catch(error => {
    root.render(
      <div className="error-screen">
        <h1>Authentication Error</h1>
        <button onClick={() => window.location.reload()}>
          Retry
        </button>
      </div>
    );
  });