import React from 'react';
import { useAuth } from '../Auth/AuthContext';
import { Navigate, Link } from 'react-router-dom';
import '../styles/Home.css';

const HomePage: React.FC = () => {
  const { isAuthenticated, keycloak } = useAuth();

  if (!isAuthenticated || !keycloak.authenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <>
      <nav className="navbar">
        <div className="navbar-container">
          <Link to="/" className="navbar-logo">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
              <path d="M2 12l10 5 10-5" />
            </svg>
            <span>CallInsights</span>
          </Link>
        </div>
      </nav>

      <header className="hero">
        <h1>
          Gain <span className="highlight">Clarity</span> Through Your Calls
        </h1>
        <p>
          Unlock the power of your call data with advanced analytics and intuitive dashboards.
        </p>
        <div className="button-group">
          <Link to="/dashboard" className="btn-primary">Get Started</Link>
        </div>
      </header>
    </>
  );
};

export default HomePage;
