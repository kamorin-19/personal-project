import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';
import { resolve } from 'path';
import { defineConfig } from 'vitest/config';

// Docker環境ではサービス名、ローカルではlocalhost
const BACKEND_HOST = process.env.BACKEND_HOST ?? 'localhost';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()] as never,
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
	},
	test: {
		include: ['src/**/*.test.{js,ts}'],
		environment: 'jsdom',
		globals: true,
		setupFiles: ['./vitest.setup.ts'],
		alias: [
			{
				find: /^svelte$/,
				replacement: resolve('./node_modules/svelte/src/index-client.js')
			}
		]
	}
});
