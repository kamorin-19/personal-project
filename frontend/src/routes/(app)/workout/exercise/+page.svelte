<svelte:head>
	<title>種目マスタ — Personal Manager</title>
</svelte:head>

<div class="px-4 py-6 lg:px-8 lg:py-10">
	<!-- パンくず -->
	<nav class="mb-6 flex items-center gap-2 text-sm text-gray-500" aria-label="パンくずリスト">
		<a href="/workout" class="hover:text-gray-700">筋トレ</a>
		<svg class="h-4 w-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
			<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
		</svg>
		<span class="font-medium text-gray-800" aria-current="page">種目マスタ</span>
	</nav>

	<div class="mb-6">
		<h1 class="text-2xl font-bold text-gray-900">種目マスタ</h1>
		<p class="mt-1 text-sm text-gray-500">トレーニング種目を登録してください</p>
	</div>

	<div class="max-w-md">
		<div class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
			<form>
				<div class="space-y-5">
					<!-- 種目名 -->
					<div>
						<label for="exercise-name" class="block text-sm font-medium text-gray-700">種目名</label>
						<input
							id="exercise-name"
							type="text"
							placeholder="例）ベンチプレス"
							class="mt-1.5 block w-full rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 shadow-sm transition-colors placeholder:text-gray-400 focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
						/>
					</div>

					<!-- 部位 -->
					<div>
						<label for="muscle-group" class="block text-sm font-medium text-gray-700">部位</label>
						<select
							id="muscle-group"
							class="mt-1.5 block w-full appearance-none rounded-xl border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 shadow-sm transition-colors focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
						>
							<option value="" disabled selected>部位を選択してください</option>
							<option value="chest">胸</option>
							<option value="back">背中</option>
							<option value="shoulder">肩</option>
							<option value="arm">腕</option>
							<option value="abdomen">腹</option>
							<option value="leg">脚</option>
							<option value="other">その他</option>
						</select>
					</div>

					<!-- 推定消費カロリー -->
					<div>
						<label for="calories-per-rep" class="block text-sm font-medium text-gray-700">
							推定消費カロリー
							<span class="ml-1 text-xs font-normal text-gray-400">（重量1kgあたり・1レップ）</span>
						</label>
						<div class="relative mt-1.5">
							<input
								id="calories-per-rep"
								type="number"
								inputmode="decimal"
								min="0"
								step="0.001"
								placeholder="0.000"
								class="block w-full rounded-xl border border-gray-300 bg-white py-2.5 pl-4 pr-20 text-sm text-gray-900 shadow-sm transition-colors focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
							/>
							<span class="pointer-events-none absolute inset-y-0 right-4 flex items-center text-sm text-gray-400">kcal</span>
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
