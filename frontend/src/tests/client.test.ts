import { describe, it, expect, vi, beforeEach } from 'vitest';

vi.mock('$env/static/private', () => ({
	BACKEND_URL: 'http://localhost:8000'
}));

vi.mock('$env/static/public', () => ({
	PUBLIC_API_URL: ''
}));

const { serverApiFetch } = await import('$lib/api/client');

describe('serverApiFetch', () => {
	beforeEach(() => {
		vi.clearAllMocks();
	});

	// C-01: ok レスポンスで JSON を返す
	it('ok レスポンスで JSON を返す', async () => {
		global.fetch = vi.fn().mockResolvedValue({
			ok: true,
			json: async () => ({ id: 1, weight: 70.5, date: '2026-04-29' })
		} as Response);

		const result = await serverApiFetch<{ id: number }>('/weights', undefined);
		expect(result).toEqual({ id: 1, weight: 70.5, date: '2026-04-29' });
	});

	// C-02: token あり: Authorization ヘッダが付与される
	it('token あり: Authorization ヘッダが付与される', async () => {
		global.fetch = vi.fn().mockResolvedValue({
			ok: true,
			json: async () => ({})
		} as Response);

		await serverApiFetch('/weights', 'abc123');

		const [, init] = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0] as [
			string,
			RequestInit
		];
		expect((init.headers as Record<string, string>)['Authorization']).toBe('Bearer abc123');
	});

	// C-03: POST + body: options が正しくマージされる
	it('POST + body: options が正しくマージされる', async () => {
		global.fetch = vi.fn().mockResolvedValue({
			ok: true,
			json: async () => ({})
		} as Response);

		const body = JSON.stringify({ weight: 70.5, date: '2026-04-29' });
		await serverApiFetch('/weights', undefined, { method: 'POST', body });

		const [, init] = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0] as [
			string,
			RequestInit
		];
		expect(init.method).toBe('POST');
		expect(init.body).toBe(body);
	});

	// C-04: Content-Type が自動付与される
	it('Content-Type が自動付与される', async () => {
		global.fetch = vi.fn().mockResolvedValue({
			ok: true,
			json: async () => ({})
		} as Response);

		await serverApiFetch('/weights', undefined);

		const [, init] = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0] as [
			string,
			RequestInit
		];
		expect((init.headers as Record<string, string>)['Content-Type']).toBe('application/json');
	});

	// C-05: BACKEND_URL がベース URL として使われる
	it('BACKEND_URL がベース URL として使われる', async () => {
		global.fetch = vi.fn().mockResolvedValue({
			ok: true,
			json: async () => ({})
		} as Response);

		await serverApiFetch('/weights', undefined);

		const [url] = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0] as [string];
		expect(url).toBe('http://localhost:8000/weights');
	});

	// C-06: ok=false で Error をスロー (404)
	it('ok=false で Error をスロー（status 404 含む）', async () => {
		global.fetch = vi.fn().mockResolvedValue({
			ok: false,
			status: 404,
			text: async () => 'Not Found'
		} as unknown as Response);

		await expect(serverApiFetch('/weights', undefined)).rejects.toThrow('404');
	});

	// C-07: ok=false で Error をスロー (500)
	it('ok=false で Error をスロー（status 500 含む）', async () => {
		global.fetch = vi.fn().mockResolvedValue({
			ok: false,
			status: 500,
			text: async () => 'Internal Server Error'
		} as unknown as Response);

		await expect(serverApiFetch('/weights', undefined)).rejects.toThrow('500');
	});

	// C-08: token が undefined: Authorization ヘッダ不付与
	it('token が undefined: Authorization ヘッダ不付与', async () => {
		global.fetch = vi.fn().mockResolvedValue({
			ok: true,
			json: async () => ({})
		} as Response);

		await serverApiFetch('/weights', undefined);

		const [, init] = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0] as [
			string,
			RequestInit
		];
		expect((init.headers as Record<string, string>)['Authorization']).toBeUndefined();
	});

	// C-09: token が空文字: Authorization ヘッダ不付与
	it('token が空文字: Authorization ヘッダ不付与', async () => {
		global.fetch = vi.fn().mockResolvedValue({
			ok: true,
			json: async () => ({})
		} as Response);

		await serverApiFetch('/weights', '');

		const [, init] = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0] as [
			string,
			RequestInit
		];
		expect((init.headers as Record<string, string>)['Authorization']).toBeUndefined();
	});
});
