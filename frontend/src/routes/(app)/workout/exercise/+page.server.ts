import { fail } from '@sveltejs/kit';
import { serverApiFetch } from '$lib/api/client';
import type { ExerciseResponse } from '$lib/api/generated/types.gen';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies }) => {
	const token = cookies.get('session');
	if (!token) return { exercises: [] as ExerciseResponse[] };

	try {
		const data = await serverApiFetch<{ items: ExerciseResponse[] }>(
			'/workout/exercise',
			token
		);
		return { exercises: data.items };
	} catch (err) {
		return { exercises: [] as ExerciseResponse[] };
	}
};

export const actions: Actions = {
	create: async ({ request, cookies }) => {
		const token = cookies.get('session');
		if (!token) return fail(401, { error: '認証が必要です' });

		const formData = await request.formData();
		const name = formData.get('name') as string;
		const muscle_group = formData.get('muscle_group') as string;
		const calories_str = formData.get('calories_per_rep_per_kg') as string;

		if (!name || !muscle_group) {
			return fail(400, { error: '種目名と部位は必須です' });
		}

		const calories_per_rep_per_kg = calories_str && !isNaN(parseFloat(calories_str))
			? parseFloat(calories_str)
			: null;

		try {
			await serverApiFetch<ExerciseResponse>(
				'/workout/exercise',
				token,
				{
					method: 'POST',
					body: JSON.stringify({ name, muscle_group, calories_per_rep_per_kg })
				}
			);
			return { success: true };
		} catch (err) {
			const errorMsg = err instanceof Error ? err.message : '登録に失敗しました';
			return fail(400, { error: errorMsg });
		}
	},

	delete: async ({ request, cookies }) => {
		const token = cookies.get('session');
		if (!token) return fail(401, { error: '認証が必要です' });

		const formData = await request.formData();
		const exercise_id = formData.get('exercise_id') as string;

		try {
			await serverApiFetch<void>(
				`/workout/exercise/${exercise_id}`,
				token,
				{ method: 'DELETE' }
			);
			return { success: true };
		} catch (err) {
			const errorMsg = err instanceof Error ? err.message : '削除に失敗しました';
			// 404エラーは成功と同等に扱う
			if (errorMsg.includes('404')) {
				return { success: true };
			}
			return fail(400, { error: errorMsg });
		}
	}
};
