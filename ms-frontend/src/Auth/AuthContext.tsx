import React, { createContext, useContext, useEffect, useState } from 'react';
import authService from './Keyclock';
import Keycloak from 'keycloak-js';

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  keycloak: Keycloak;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const [state, setState] = useState({
    isAuthenticated: false,
    isLoading: true
  });

  const [initialized, setInitialized] = useState(false);
  const keycloak = authService.getKeycloakInstance();

  useEffect(() => {
    if (initialized) return;

    const updateAuthState = () => {
      setState({
        isAuthenticated: !!keycloak.authenticated,
        isLoading: false
      });
    };

    keycloak.onAuthSuccess = updateAuthState;
    keycloak.onAuthRefreshSuccess = updateAuthState;
    keycloak.onAuthLogout = () => setState({ isAuthenticated: false, isLoading: false });

    updateAuthState();
    setInitialized(true);

    return () => {
      keycloak.onAuthSuccess = undefined;
      keycloak.onAuthRefreshSuccess = undefined;
      keycloak.onAuthLogout = undefined;
    };
  }, [initialized, keycloak]);

  return (
    <AuthContext.Provider value={{
      isAuthenticated: state.isAuthenticated,
      isLoading: state.isLoading,
      keycloak
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};