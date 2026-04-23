import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
	input: '../backend/openapi.json',
	output: {
		path: 'src/lib/api/generated',
		format: 'prettier'
	},
	client: 'fetch'
});
