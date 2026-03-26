import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    port: 5173,
    proxy: {
      '/events': 'http://localhost:8899',
      '/ledger': 'http://localhost:8899',
      '/moderator': 'http://localhost:8899',
      '/questions': 'http://localhost:8899',
    },
  },
})
