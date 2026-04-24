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
		<div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
			<form>
				<div class="space-y-5">
					<!-- 日付 -->
					<div>
						<label for="log-date" class="block text-sm font-medium text-gray-700">日付</label>
						<input
							id="log-date"
							type="date"
							class="mt-1.5 block w-full rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 shadow-sm transition-colors focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
						/>
					</div>

					<!-- 種目名 -->
					<div>
						<label for="exercise-name" class="block text-sm font-medium text-gray-700">種目名</label>
						<select
							id="exercise-name"
							class="mt-1.5 block w-full appearance-none rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 shadow-sm transition-colors focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
						>
							<option value="" disabled selected>種目を選択してください</option>
							<optgroup label="胸">
								<option value="bench-press">ベンチプレス</option>
								<option value="incline-bench-press">インクラインベンチプレス</option>
								<option value="dumbbell-fly">ダンベルフライ</option>
							</optgroup>
							<optgroup label="背中">
								<option value="deadlift">デッドリフト</option>
								<option value="barbell-row">バーベルロウ</option>
								<option value="lat-pulldown">ラットプルダウン</option>
							</optgroup>
							<optgroup label="肩">
								<option value="overhead-press">オーバーヘッドプレス</option>
								<option value="lateral-raise">サイドレイズ</option>
							</optgroup>
							<optgroup label="腕">
								<option value="barbell-curl">バーベルカール</option>
								<option value="triceps-pushdown">トライセプスプッシュダウン</option>
							</optgroup>
							<optgroup label="脚">
								<option value="squat">スクワット</option>
								<option value="leg-press">レッグプレス</option>
								<option value="leg-curl">レッグカール</option>
							</optgroup>
						</select>
					</div>

					<!-- 重量 -->
					<div>
						<label for="weight" class="block text-sm font-medium text-gray-700">重量</label>
						<div class="relative mt-1.5">
							<input
								id="weight"
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
