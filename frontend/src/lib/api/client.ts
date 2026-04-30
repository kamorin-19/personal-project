import { PUBLIC_API_URL } from '$env/static/public';
import { BACKEND_URL } from '$env/static/private';

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
	const url = `${PUBLIC_API_URL}${path}`;
	const res = await fetch(url, {
		headers: { 'Content-Type': 'application/json', ...options.headers },
		...options
	});

	if (!res.ok) {
		const error = await res.text();
		throw new Error(`API error ${res.status}: ${error}`);
	}

	return res.json() as Promise<T>;
}

export async function serverApiFetch<T>(
	path: string,
	token: string | undefined,
	options: RequestInit = {}
): Promise<T> {
	const url = `${BACKEND_URL}${path}`;
	const baseHeaders: Record<string, string> = {
		'Content-Type': 'application/json',
		...(token ? { Authorization: `Bearer ${token}` } : {})
	};
	const headers = options.headers
		? { ...baseHeaders, ...Object.fromEntries(new Headers(options.headers).entries()) }
		: baseHeaders;
	const res = await fetch(url, { ...options, headers });

	if (!res.ok) {
		const error = await res.text();
		throw new Error(`API error ${res.status}: ${error}`);
	}

	return res.json() as Promise<T>;
}
