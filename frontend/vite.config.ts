import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';

// Docker環境ではサービス名、ローカルではlocalhost
const BACKEND_HOST = process.env.BACKEND_HOST ?? 'localhost';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	server: {
		host: '0.0.0.0',
		port: 5173,
		proxy: {
			'/api': {
				target: `http://${BACKEND_HOST}:8000`,
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/api/, '')
			}
		},
		watch: {
			usePolling: true
		}
	}
});
