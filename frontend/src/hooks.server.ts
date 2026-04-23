import type { Handle } from '@sveltejs/kit';
import { jwtVerify } from 'jose';
import { JWT_SECRET } from '$env/static/private';

const secret = new TextEncoder().encode(JWT_SECRET);

export const handle: Handle = async ({ event, resolve }) => {
	const token = event.cookies.get('session');

	if (token) {
		try {
			const { payload } = await jwtVerify(token, secret);
			event.locals.user = {
				userId: payload.sub as string,
				email: payload['email'] as string,
				name: (payload['name'] as string | undefined) ?? null
			};
		} catch {
			event.cookies.delete('session', { path: '/' });
			event.locals.user = null;
		}
	} else {
		event.locals.user = null;
	}

	return resolve(event);
};
