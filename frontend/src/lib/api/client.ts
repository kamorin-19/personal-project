import { PUBLIC_API_URL } from '$env/static/public';

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
