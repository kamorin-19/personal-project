import { fail } from '@sveltejs/kit';
import { BACKEND_URL } from '$env/static/private';
import type { ExerciseResponse } from '$lib/api/generated/types.gen';
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
	if (!token) return { exercises: [] as ExerciseResponse[] };

	const res = await fetch(backendUrl('/workout/exercise'), {
		headers: authHeaders(token)
	});

	if (!res.ok) return { exercises: [] as ExerciseResponse[] };

	const data = (await res.json()) as { items: ExerciseResponse[] };
	return { exercises: data.items };
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

		const calories_per_rep_per_kg = calories_str ? parseFloat(calories_str) : null;

		const res = await fetch(backendUrl('/workout/exercise'), {
			method: 'POST',
			headers: authHeaders(token),
			body: JSON.stringify({ name, muscle_group, calories_per_rep_per_kg })
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
		const exercise_id = formData.get('exercise_id') as string;

		const res = await fetch(backendUrl(`/workout/exercise/${exercise_id}`), {
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
