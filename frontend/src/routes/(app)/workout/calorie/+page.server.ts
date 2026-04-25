import { fail } from '@sveltejs/kit';
import { BACKEND_URL } from '$env/static/private';
import type { CalorieLogResponse } from '$lib/api/generated/types.gen';
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
	if (!token) return { records: [] as CalorieLogResponse[] };

	const res = await fetch(backendUrl('/workout/calorie'), {
		headers: authHeaders(token)
	});

	if (!res.ok) return { records: [] as CalorieLogResponse[] };

	const data = (await res.json()) as { items: CalorieLogResponse[] };
	return { records: data.items };
};

export const actions: Actions = {
	upsert: async ({ request, cookies }) => {
		const token = cookies.get('session');
		if (!token) return fail(401, { error: '認証が必要です' });

		const formData = await request.formData();
		const record_date = formData.get('record_date') as string;
		const calories_str = formData.get('calories') as string;

		if (!record_date || !calories_str) {
			return fail(400, { error: '日付とカロリーは必須です' });
		}

		const calories = parseInt(calories_str, 10);
		if (isNaN(calories)) {
			return fail(400, { error: 'カロリーは整数で入力してください' });
		}

		const res = await fetch(backendUrl('/workout/calorie'), {
			method: 'POST',
			headers: authHeaders(token),
			body: JSON.stringify({ record_date, calories })
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

		const res = await fetch(backendUrl(`/workout/calorie/${record_date}`), {
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
