import { redirect, error } from '@sveltejs/kit';
import { randomBytes, createHash } from 'crypto';
import { dev } from '$app/environment';
import { SignJWT } from 'jose';
import type { PageServerLoad, Actions } from './$types';
import { PUBLIC_GOOGLE_CLIENT_ID } from '$env/static/public';
import { GOOGLE_REDIRECT_URI, JWT_SECRET } from '$env/static/private';

export const load: PageServerLoad = ({ locals }) => {
	if (locals.user) {
		redirect(302, '/');
	}
	return { dev };
};

export const actions: Actions = {
	// Google OAuth フロー (本番用)
	googleLogin: ({ cookies }) => {
		const state = randomBytes(16).toString('hex');
		const codeVerifier = randomBytes(32).toString('base64url');
		const codeChallenge = createHash('sha256').update(codeVerifier).digest('base64url');

		const cookieOpts = {
			path: '/',
			httpOnly: true,
			sameSite: 'lax' as const,
			maxAge: 600
		};
		cookies.set('oauth_state', state, cookieOpts);
		cookies.set('oauth_verifier', codeVerifier, cookieOpts);

		const params = new URLSearchParams({
			client_id: PUBLIC_GOOGLE_CLIENT_ID,
			redirect_uri: GOOGLE_REDIRECT_URI,
			response_type: 'code',
			scope: 'openid email profile',
			state,
			code_challenge: codeChallenge,
			code_challenge_method: 'S256',
			access_type: 'offline',
			prompt: 'select_account'
		});

		redirect(302, `https://accounts.google.com/o/oauth2/v2/auth?${params}`);
	},

	// 開発環境専用バイパス — 本番では 403 を返す
	devLogin: async ({ cookies }) => {
		if (!dev) {
			error(403, '本番環境では開発用ログインは使用できません');
		}

		const secret = new TextEncoder().encode(JWT_SECRET);
		const token = await new SignJWT({
			email: 'dev@example.com',
			name: '開発ユーザー'
		})
			.setProtectedHeader({ alg: 'HS256' })
			.setSubject('dev-user-id')
			.setIssuedAt()
			.setExpirationTime('24h')
			.sign(secret);

		cookies.set('session', token, {
			path: '/',
			httpOnly: true,
			secure: false,
			sameSite: 'lax',
			maxAge: 60 * 60 * 24
		});

		redirect(302, '/');
	}
};
