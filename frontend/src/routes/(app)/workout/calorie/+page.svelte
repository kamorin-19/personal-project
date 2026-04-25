<script lang="ts">
	import { enhance } from '$app/forms';
	import type { CalorieLogResponse } from '$lib/api/generated/types.gen';
	import type { PageData, ActionData } from './$types';

	let { data, form }: { data: PageData; form: ActionData } = $props();

	let records = $derived((data?.records ?? []) as CalorieLogResponse[]);
	let submitting = $state(false);
</script>

<svelte:head>
	<title>摂取カロリー記録 — Personal Manager</title>
</svelte:head>

<div class="px-4 py-6 lg:px-8 lg:py-10">
	<!-- パンくず -->
	<nav class="mb-6 flex items-center gap-2 text-sm text-gray-500" aria-label="パンくずリスト">
		<a href="/workout" class="hover:text-gray-700">筋トレ</a>
		<svg class="h-4 w-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
			<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
		</svg>
		<span class="font-medium text-gray-800" aria-current="page">摂取カロリー記録</span>
	</nav>

	<div class="mb-6">
		<h1 class="text-2xl font-bold text-gray-900">摂取カロリー記録</h1>
		<p class="mt-1 text-sm text-gray-500">日々の摂取カロリーを入力してください</p>
	</div>

	<div class="max-w-md">
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
				action="?/upsert"
				use:enhance={() => {
					submitting = true;
					return async ({ update }) => {
						await update();
						submitting = false;
					};
				}}
			>
				<div class="space-y-5">
					<!-- 日付 -->
					<div>
						<label for="record-date" class="block text-sm font-medium text-gray-700">日付</label>
						<input
							id="record-date"
							name="record_date"
							type="date"
							required
							class="mt-1.5 block w-full rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 shadow-sm transition-colors focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
						/>
					</div>

					<!-- 摂取カロリー -->
					<div>
						<label for="calories" class="block text-sm font-medium text-gray-700">摂取カロリー</label>
						<div class="relative mt-1.5">
							<input
								id="calories"
								name="calories"
								type="number"
								inputmode="numeric"
								min="0"
								max="99999"
								step="1"
								placeholder="0"
								required
								class="block w-full rounded-xl border border-gray-300 bg-white py-2.5 pl-4 pr-14 text-sm text-gray-900 shadow-sm transition-colors focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
							/>
							<span class="pointer-events-none absolute inset-y-0 right-4 flex items-center text-sm text-gray-400">kcal</span>
						</div>
					</div>
				</div>

				<!-- ボタン -->
				<div class="mt-7 flex gap-3">
					<button
						type="submit"
						disabled={submitting}
						class="flex-1 rounded-xl bg-gradient-to-r from-orange-400 to-rose-500 px-4 py-2.5 text-sm font-semibold text-white shadow-sm shadow-orange-500/20 transition-all hover:from-orange-500 hover:to-rose-600 hover:shadow-md focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-500 active:scale-[0.98] disabled:opacity-60"
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
		{#if records.length > 0}
			<div class="mt-6">
				<h2 class="mb-3 text-sm font-semibold text-gray-700">記録一覧</h2>
				<div class="space-y-2">
					{#each records as record (record.record_date)}
						<div class="flex items-center justify-between rounded-xl border border-gray-200 bg-white px-4 py-3 shadow-sm">
							<div>
								<p class="text-sm font-medium text-gray-900">{record.record_date}</p>
								<p class="mt-0.5 text-xs text-gray-500">{record.calories.toLocaleString()} kcal</p>
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
								<input type="hidden" name="record_date" value={record.record_date} />
								<button
									type="submit"
									class="rounded-lg p-1.5 text-gray-400 transition-colors hover:bg-red-50 hover:text-red-500"
									aria-label="{record.record_date}の記録を削除"
								>
									<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
										<path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
									</svg>
								</button>
							</form>
						</div>
					{/each}
				</div>
			</div>
		{/if}
	</div>
</div>
