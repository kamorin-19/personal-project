<svelte:head>
	<title>体重記録 — Personal Manager</title>
</svelte:head>

<div class="px-4 py-6 lg:px-8 lg:py-10">
	<!-- パンくず -->
	<nav class="mb-6 flex items-center gap-2 text-sm text-gray-500" aria-label="パンくずリスト">
		<a href="/workout" class="hover:text-gray-700">筋トレ</a>
		<svg class="h-4 w-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
			<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
		</svg>
		<span class="font-medium text-gray-800" aria-current="page">体重記録</span>
	</nav>

	<div class="mb-6">
		<h1 class="text-2xl font-bold text-gray-900">体重記録</h1>
		<p class="mt-1 text-sm text-gray-500">日々の体重・体脂肪率を入力してください</p>
	</div>

	<div class="max-w-md">
		<div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
			<form>
				<div class="space-y-5">
					<!-- 日付 -->
					<div>
						<label for="date" class="block text-sm font-medium text-gray-700">日付</label>
						<input
							id="date"
							type="date"
							class="mt-1.5 block w-full rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 shadow-sm transition-colors focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
						/>
					</div>

					<!-- 体重 -->
					<div>
						<label for="weight" class="block text-sm font-medium text-gray-700">体重</label>
						<div class="relative mt-1.5">
							<input
								id="weight"
								type="number"
								inputmode="decimal"
								min="0"
								max="300"
								step="0.1"
								placeholder="0.0"
								class="block w-full rounded-xl border border-gray-300 bg-white py-2.5 pl-4 pr-12 text-sm text-gray-900 shadow-sm transition-colors focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
							/>
							<span class="pointer-events-none absolute inset-y-0 right-4 flex items-center text-sm text-gray-400">kg</span>
						</div>
					</div>

					<!-- 体脂肪率 -->
					<div>
						<label for="body-fat" class="block text-sm font-medium text-gray-700">体脂肪率</label>
						<div class="relative mt-1.5">
							<input
								id="body-fat"
								type="number"
								inputmode="decimal"
								min="0"
								max="100"
								step="0.1"
								placeholder="0.0"
								class="block w-full rounded-xl border border-gray-300 bg-white py-2.5 pl-4 pr-10 text-sm text-gray-900 shadow-sm transition-colors focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
							/>
							<span class="pointer-events-none absolute inset-y-0 right-4 flex items-center text-sm text-gray-400">%</span>
						</div>
					</div>
				</div>

				<!-- ボタン -->
				<div class="mt-7 flex gap-3">
					<button
						type="submit"
						class="flex-1 rounded-xl bg-gradient-to-r from-orange-400 to-rose-500 px-4 py-2.5 text-sm font-semibold text-white shadow-sm shadow-orange-500/20 transition-all hover:from-orange-500 hover:to-rose-600 hover:shadow-md focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-orange-500 active:scale-[0.98]"
					>
						登録
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
	</div>
</div>
