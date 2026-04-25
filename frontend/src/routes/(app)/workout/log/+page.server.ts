import { fail } from '@sveltejs/kit';
import { BACKEND_URL } from '$env/static/private';
import type { ExerciseResponse, WorkoutLogResponse } from '$lib/api/generated/types.gen';
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
	if (!token) {
		return {
			exercises: [] as ExerciseResponse[],
			logs: [] as WorkoutLogResponse[]
		};
	}

	const [exercisesRes, logsRes] = await Promise.all([
		fetch(backendUrl('/workout/exercise'), { headers: authHeaders(token) }),
		fetch(backendUrl('/workout/log'), { headers: authHeaders(token) })
	]);

	const exercises = exercisesRes.ok
		? ((await exercisesRes.json()) as { items: ExerciseResponse[] }).items
		: ([] as ExerciseResponse[]);

	const logs = logsRes.ok
		? ((await logsRes.json()) as { items: WorkoutLogResponse[] }).items
		: ([] as WorkoutLogResponse[]);

	return { exercises, logs };
};

export const actions: Actions = {
	create: async ({ request, cookies }) => {
		const token = cookies.get('session');
		if (!token) return fail(401, { error: '認証が必要です' });

		const formData = await request.formData();
		const record_date = formData.get('record_date') as string;
		const exercise_id = formData.get('exercise_id') as string;
		const exercise_name = formData.get('exercise_name') as string;
		const weight_kg_str = formData.get('weight_kg') as string;

		if (!record_date || !exercise_id || !exercise_name) {
			return fail(400, { error: '日付と種目は必須です' });
		}

		const setsRaw: number[] = [];
		for (let i = 1; i <= 10; i++) {
			const val = formData.get(`set_${i}`) as string;
			if (val && val.trim() !== '') {
				const n = parseInt(val, 10);
				if (!isNaN(n)) setsRaw.push(n);
			}
		}

		if (setsRaw.length === 0) {
			return fail(400, { error: 'セット回数を1つ以上入力してください' });
		}

		const weight_kg = weight_kg_str ? parseFloat(weight_kg_str) : null;

		const res = await fetch(backendUrl('/workout/log'), {
			method: 'POST',
			headers: authHeaders(token),
			body: JSON.stringify({ record_date, exercise_id, exercise_name, weight_kg, sets: setsRaw })
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
		const log_id = formData.get('log_id') as string;

		const res = await fetch(backendUrl(`/workout/log/${log_id}`), {
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
