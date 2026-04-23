import { redirect, error } from '@sveltejs/kit';
import { dev } from '$app/environment';
import type { RequestHandler } from './$types';
import { BACKEND_URL } from '$env/static/private';

export const GET: RequestHandler = async ({ url, cookies, fetch }) => {
	const code = url.searchParams.get('code');
	const state = url.searchParams.get('state');
	const errorParam = url.searchParams.get('error');

	if (errorParam) {
		redirect(302, `/login?error=${encodeURIComponent(errorParam)}`);
	}

	const storedState = cookies.get('oauth_state');
	const codeVerifier = cookies.get('oauth_verifier');

	// CSRF チェック
	if (!state || state !== storedState) {
		error(400, 'セキュリティエラー: state パラメータが一致しません');
	}
	if (!code || !codeVerifier) {
		error(400, '認証コードまたはベリファイアが見つかりません');
	}

	cookies.delete('oauth_state', { path: '/' });
	cookies.delete('oauth_verifier', { path: '/' });

	// FastAPI にコード交換を依頼
	const res = await fetch(`${BACKEND_URL}/auth/google/callback`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ code, code_verifier: codeVerifier })
	});

	if (!res.ok) {
		const detail = await res.text().catch(() => '');
		console.error('Auth callback failed:', res.status, detail);
		error(500, '認証に失敗しました。もう一度お試しください。');
	}

	const { token } = (await res.json()) as { token: string };

	cookies.set('session', token, {
		path: '/',
		httpOnly: true,
		secure: !dev,
		sameSite: 'lax',
		maxAge: 60 * 60 * 24 // 24時間
	});

	redirect(302, '/');
};
