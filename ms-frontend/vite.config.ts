import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
    build: {
    // Ignore TypeScript errors during build
    sourcemap: true,
    chunkSizeWarningLimit: 1000,
    rollupOptions: {
      onwarn(warning, warn) {
        // Ignore certain warnings
        if (warning.code === 'THIS_IS_UNDEFINED') return;
        if (warning.code === 'UNUSED_EXTERNAL_IMPORT') return;
        warn(warning);
      }
    }
  },
  server: {
    proxy: {
      '/realms': 'http://localhost:8081',
      '/auth': 'http://localhost:8081',
      '/keycloak': 'http://localhost:8081',
      '/admin': 'http://localhost:8081',
      '/auth/realms': 'http://localhost:8081',
      '/auth/admin': 'http://localhost:8081',
      '/auth/realms/cdr-platform': 'http://localhost:8081',
      '/auth/realms/cdr-platform/protocol': 'http://localhost:8081',
      '/api': {
        target: 'http://localhost:5500',
        changeOrigin: true,
        secure: false, // If the target server uses HTTPS, set this to true
        ws: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
    

    },
    port: 4000,
  }

})
