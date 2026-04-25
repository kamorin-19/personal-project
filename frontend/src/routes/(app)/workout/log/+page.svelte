<script lang="ts">
	import { enhance } from '$app/forms';
	import type { ExerciseResponse, WorkoutLogResponse } from '$lib/api/generated/types.gen';
	import type { PageData, ActionData } from './$types';

	let { data, form }: { data: PageData; form: ActionData } = $props();

	let exercises = $derived((data?.exercises ?? []) as ExerciseResponse[]);
	let logs = $derived((data?.logs ?? []) as WorkoutLogResponse[]);
	let submitting = $state(false);

	const muscleGroupLabel: Record<string, string> = {
		chest: '胸',
		back: '背中',
		shoulder: '肩',
		arm: '腕',
		abdomen: '腹',
		leg: '脚',
		other: 'その他'
	};

	const muscleGroupOrder = ['chest', 'back', 'shoulder', 'arm', 'abdomen', 'leg', 'other'];

	type ExerciseGroup = { group: string; label: string; items: ExerciseResponse[] };

	let exerciseGroups = $derived(
		muscleGroupOrder
			.map((group) => ({
				group,
				label: muscleGroupLabel[group] ?? group,
				items: exercises.filter((e) => e.muscle_group === group)
			}))
			.filter((g): g is ExerciseGroup => g.items.length > 0)
	);

	let selectedExerciseId = $state('');
	let selectedExerciseName = $state('');

	function onExerciseChange(e: Event) {
		const select = e.currentTarget as HTMLSelectElement;
		const option = select.selectedOptions[0];
		selectedExerciseId = option?.value ?? '';
		selectedExerciseName = option?.dataset.name ?? '';
	}

	function formatSets(sets: number[]): string {
		return sets.join(', ') + ' 回';
	}
</script>

<svelte:head>
	<title>日々の記録 — Personal Manager</title>
</svelte:head>

<div class="px-4 py-6 lg:px-8 lg:py-10">
	<!-- パンくず -->
	<nav class="mb-6 flex items-center gap-2 text-sm text-gray-500" aria-label="パンくずリスト">
		<a href="/workout" class="hover:text-gray-700">筋トレ</a>
		<svg class="h-4 w-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
			<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
		</svg>
		<span class="font-medium text-gray-800" aria-current="page">日々の記録</span>
	</nav>

	<div class="mb-6">
		<h1 class="text-2xl font-bold text-gray-900">日々の記録</h1>
		<p class="mt-1 text-sm text-gray-500">トレーニングの種目・重量・セット回数を入力してください</p>
	</div>

	<div class="max-w-lg">
		<!-- 入力フォーム -->
		<div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
			{#if form?.error}
				<div
					class="mb-4 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
					role="alert"
				>
					{form.error}
				</div>
			{/if}

			{#if form?.success}
				<div
					class="mb-4 rounded-xl border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700"
					role="status"
				>
					登録しました
				</div>
			{/if}

			<form
				method="POST"
				action="?/create"
				use:enhance={() => {
					submitting = true;
					return async ({ update }) => {
						await update();
						submitting = false;
					};
				}}
			>
				<input type="hidden" name="exercise_id" value={selectedExerciseId} />
				<input type="hidden" name="exercise_name" value={selectedExerciseName} />

				<div class="space-y-5">
					<!-- 日付 -->
					<div>
						<label for="log-date" class="block text-sm font-medium text-gray-700">日付</label>
						<input
							id="log-date"
							name="record_date"
							type="date"
							required
							class="mt-1.5 block w-full rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 shadow-sm transition-colors focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
						/>
					</div>

					<!-- 種目名 -->
					<div>
						<label for="exercise-select" class="block text-sm font-medium text-gray-700">種目名</label>
						{#if exercises.length === 0}
							<p class="mt-1.5 text-sm text-gray-400">
								種目が登録されていません。<a href="/workout/exercise" class="text-orange-500 underline hover:text-orange-600">種目マスタ</a>から登録してください。
							</p>
						{:else}
							<select
								id="exercise-select"
								required
								onchange={onExerciseChange}
								class="mt-1.5 block w-full appearance-none rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 shadow-sm transition-colors focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
							>
								<option value="" disabled selected>種目を選択してください</option>
								{#each exerciseGroups as group (group.group)}
									<optgroup label={group.label}>
										{#each group.items as exercise (exercise.exercise_id)}
											<option value={exercise.exercise_id} data-name={exercise.name}>
												{exercise.name}
											</option>
										{/each}
									</optgroup>
								{/each}
							</select>
						{/if}
					</div>

					<!-- 重量 -->
					<div>
						<label for="weight" class="block text-sm font-medium text-gray-700">重量</label>
						<div class="relative mt-1.5">
							<input
								id="weight"
								name="weight_kg"
								type="number"
								inputmode="decimal"
								min="0"
								max="999"
								step="0.5"
								placeholder="0.0"
								class="block w-full rounded-xl border border-gray-300 bg-white py-2.5 pl-4 pr-12 text-sm text-gray-900 shadow-sm transition-colors focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
							/>
							<span class="pointer-events-none absolute inset-y-0 right-4 flex items-center text-sm text-gray-400">kg</span>
						</div>
					</div>

					<!-- セット別回数 -->
					<div>
						<p class="block text-sm font-medium text-gray-700">セット別回数</p>
						<p class="mt-0.5 text-xs text-gray-400">実施しないセットは空欄のままにしてください</p>
						<div class="mt-3 grid grid-cols-5 gap-x-3 gap-y-4">
							{#each Array(10) as _, i}
								<div class="flex flex-col items-center gap-1">
									<label
										for="set-{i + 1}"
										class="text-xs font-medium text-gray-500"
									>
										セット{i + 1}
									</label>
									<div class="relative w-full">
										<input
											id="set-{i + 1}"
											name="set_{i + 1}"
											type="number"
											inputmode="numeric"
											min="0"
											max="999"
											step="1"
											placeholder="—"
											class="block w-full rounded-lg border border-gray-300 bg-white py-2 pl-2 pr-5 text-center text-sm text-gray-900 shadow-sm transition-colors placeholder:text-gray-300 focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
										/>
										<span class="pointer-events-none absolute inset-y-0 right-1.5 flex items-center text-xs text-gray-400">回</span>
									</div>
								</div>
							{/each}
						</div>
					</div>
				</div>

				<!-- ボタン -->
				<div class="mt-7 flex gap-3">
					<button
						type="submit"
						disabled={submitting}
						class="flex-1 rounded-xl bg-gradient-to-r from-orange-400 to-rose-500 px-4 py-2.5 text-sm font-semibold text-white shadow-sm shadow-orange-500/20 transition-all hover:from-orange-500 hover:to-rose-600 hover:shadow-md focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-500 active:scale-[0.98] disabled:opacity-50"
					>
						{submitting ? '登録中…' : '登録'}
					</button>
					<button
						type="reset"
						class="flex-1 rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-sm font-semibold text-gray-600 shadow-sm transition-all hover:bg-gray-50 hover:text-gray-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-gray-400 active:scale-[0.98]"
					>
						クリア
					</button>
				</div>
			</form>
		</div>

		<!-- 記録一覧 -->
		{#if logs.length > 0}
			<div class="mt-8">
				<h2 class="mb-4 text-lg font-semibold text-gray-800">記録一覧</h2>
				<ul class="space-y-3">
					{#each logs as log (log.log_id)}
						<li class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
							<div class="flex items-start justify-between gap-3">
								<div class="min-w-0 flex-1">
									<div class="flex flex-wrap items-center gap-2">
										<span class="text-sm font-semibold text-gray-900">{log.exercise_name}</span>
										<span class="text-xs text-gray-400">{log.record_date}</span>
									</div>
									<div class="mt-1 text-sm text-gray-600">
										{#if log.weight_kg !== null}
											<span class="mr-3">{log.weight_kg} kg</span>
										{/if}
										<span>{log.sets.length}セット：{formatSets(log.sets)}</span>
									</div>
								</div>
								<form
									method="POST"
									action="?/delete"
									use:enhance={() => {
										return async ({ update }) => {
											await update();
										};
									}}
								>
									<input type="hidden" name="log_id" value={log.log_id} />
									<button
										type="submit"
										class="shrink-0 rounded-lg border border-red-200 bg-red-50 px-3 py-1.5 text-xs font-medium text-red-600 transition-colors hover:bg-red-100 hover:text-red-700"
									>
										削除
									</button>
								</form>
							</div>
						</li>
					{/each}
				</ul>
			</div>
		{/if}
	</div>
</div>
