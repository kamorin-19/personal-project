import { fail } from '@sveltejs/kit';
import { BACKEND_URL } from '$env/static/private';
import type { WeightRecordResponse } from '$lib/api/generated/types.gen';
import type { Actions, PageServerLoad } from './$types';

function backendUrl(path: string) {
	return `${BACKEND_URL}${path}`;
}

function authHeaders(token: string): Record<string, string> {
	return {
		'Content-Type': 'application/json',
		Authorization: `Bearer ${token}`
	};
}

export const load: PageServerLoad = async ({ cookies }) => {
	const token = cookies.get('session');
	if (!token) return { records: [] as WeightRecordResponse[] };

	const res = await fetch(backendUrl('/workout/weight'), {
		headers: authHeaders(token)
	});

	if (!res.ok) return { records: [] as WeightRecordResponse[] };

	const data = (await res.json()) as { items: WeightRecordResponse[] };
	return { records: data.items };
};

export const actions: Actions = {
	upsert: async ({ request, cookies }) => {
		const token = cookies.get('session');
		if (!token) return fail(401, { error: '認証が必要です' });

		const formData = await request.formData();
		const record_date = formData.get('record_date') as string;
		const weight_kg_str = formData.get('weight_kg') as string;
		const body_fat_pct_str = formData.get('body_fat_pct') as string;

		if (!record_date || !weight_kg_str) {
			return fail(400, { error: '日付と体重は必須です' });
		}

		const weight_kg = parseFloat(weight_kg_str);
		const body_fat_pct = body_fat_pct_str ? parseFloat(body_fat_pct_str) : null;

		const res = await fetch(backendUrl('/workout/weight'), {
			method: 'POST',
			headers: authHeaders(token),
			body: JSON.stringify({ record_date, weight_kg, body_fat_pct })
		});

		if (!res.ok) {
			const errorText = await res.text().catch(() => '登録に失敗しました');
			return fail(res.status, { error: errorText });
		}

		return { success: true };
	},

	delete: async ({ request, cookies }) => {
		const token = cookies.get('session');
		if (!token) return fail(401, { error: '認証が必要です' });

		const formData = await request.formData();
		const record_date = formData.get('record_date') as string;

		const res = await fetch(backendUrl(`/workout/weight/${record_date}`), {
			method: 'DELETE',
			headers: authHeaders(token)
		});

		if (!res.ok && res.status !== 404) {
			const errorText = await res.text().catch(() => '削除に失敗しました');
			return fail(res.status, { error: errorText });
		}

		return { success: true };
	}
};
