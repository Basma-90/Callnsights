import Keycloak from 'keycloak-js';

class AuthService {
  private static instance: AuthService;
  private keycloak: Keycloak;
  private isInitialized = false;
  private initPromise: Promise<boolean> | null = null;

  private constructor() {
    this.keycloak = new Keycloak({
      url: import.meta.env.VITE_KEYCLOAK_URL || 'http://localhost:8081',
      realm: import.meta.env.VITE_KEYCLOAK_REALM || 'cdr-platform',
      clientId: import.meta.env.VITE_KEYCLOAK_CLIENT_ID || 'ms-frontend'
    });
  }

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  public async init(): Promise<boolean> {
    if (this.isInitialized) {
      return this.keycloak.authenticated || false;
    }

    if (this.initPromise) {
      return this.initPromise;
    }

    this.initPromise = this.keycloak.init({
      onLoad: 'login-required',
      checkLoginIframe: false,
      pkceMethod: 'S256'
    }).then(authenticated => {
      this.isInitialized = true;
      if (authenticated) {
        const updateToken = () => {
          const expiresIn = (this.keycloak.tokenParsed?.exp || 0) - Math.floor(Date.now() / 1000);

          if (expiresIn < 30) {
            this.keycloak.updateToken(30).catch(() => {
              this.keycloak.login();
            });
          }
        };
        const refreshInterval = setInterval(updateToken, 10000);
      }
      return authenticated;
    }).catch(error => {
      this.initPromise = null;
      throw error;
    });

    return this.initPromise;
  }

  public getKeycloakInstance(): Keycloak {
    if (!this.isInitialized) {
      throw new Error('Keycloak not initialized. Call init() first.');
    }
    return this.keycloak;
  }
}

export default AuthService.getInstance();