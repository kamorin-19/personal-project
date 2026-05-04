import { fail } from '@sveltejs/kit';
import { serverApiFetch } from '$lib/api/client';
import type { WeightRecordResponse } from '$lib/api/generated/types.gen';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies }) => {
	const token = cookies.get('session');
	if (!token) return { records: [] as WeightRecordResponse[] };

	try {
		const data = await serverApiFetch<{ items: WeightRecordResponse[] }>(
			'/workout/weight',
			token
		);
		return { records: data.items };
	} catch {
		return { records: [] as WeightRecordResponse[] };
	}
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
		if (isNaN(weight_kg) || weight_kg <= 0) {
			return fail(400, { error: '体重の値が不正です' });
		}

		const body_fat_pct = body_fat_pct_str ? parseFloat(body_fat_pct_str) : null;
		if (body_fat_pct !== null && (isNaN(body_fat_pct) || body_fat_pct < 0)) {
			return fail(400, { error: '体脂肪率の値が不正です' });
		}

		try {
			await serverApiFetch<unknown>('/workout/weight', token, {
				method: 'POST',
				body: JSON.stringify({ record_date, weight_kg, body_fat_pct })
			});
		} catch (e) {
			return fail(500, { error: e instanceof Error ? e.message : '登録に失敗しました' });
		}

		return { success: true };
	},

	delete: async ({ request, cookies }) => {
		const token = cookies.get('session');
		if (!token) return fail(401, { error: '認証が必要です' });

		const formData = await request.formData();
		const record_date = formData.get('record_date') as string;

		try {
			await serverApiFetch<unknown>(`/workout/weight/${record_date}`, token, {
				method: 'DELETE'
			});
		} catch (e) {
			const msg = e instanceof Error ? e.message : '削除に失敗しました';
			if (!msg.includes('404')) return fail(500, { error: msg });
		}

		return { success: true };
	}
};
