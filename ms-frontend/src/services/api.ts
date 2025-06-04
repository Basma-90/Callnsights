import axios from 'axios';
import authService from '../Auth/Keyclock';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5500/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
 
});

api.interceptors.request.use((config) => {
  const keycloak = authService.getKeycloakInstance();
  config.headers.Authorization = `Bearer ${keycloak.token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        await authService.init();
        const keycloak = authService.getKeycloakInstance();
        if (keycloak.isTokenExpired()) {
          await keycloak.updateToken(30);
        }

        originalRequest.headers.Authorization = `Bearer ${keycloak.token}`;
        return api(originalRequest);
      } catch (refreshError) {
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

setInterval(() => {
  const keycloak = authService.getKeycloakInstance();
  if (keycloak) {
    keycloak.updateToken(30).catch((error) => {
      keycloak.login();
    });
  }
}, 60000);

export default api;
