<svelte:head>
	<title>筋トレ — Personal Manager</title>
</svelte:head>

<div class="px-4 py-6 lg:px-8 lg:py-10">
	<div class="mb-6">
		<h1 class="text-2xl font-bold text-gray-900">筋トレ</h1>
		<p class="mt-1 text-sm text-gray-500">トレーニング記録・メニュー管理</p>
	</div>

	<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
		<a
			href="/workout/weight"
			class="group flex items-center gap-4 rounded-2xl border border-orange-100 bg-white p-5 shadow-sm transition-all hover:border-orange-200 hover:shadow-md"
		>
			<div
				class="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-orange-400 to-rose-500 shadow-md shadow-orange-500/20 transition-transform group-hover:scale-105"
			>
				<svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
					<path stroke-linecap="round" stroke-linejoin="round" d="M3 6h18M3 12h18M3 18h18" />
				</svg>
			</div>
			<div class="min-w-0">
				<p class="text-sm font-semibold text-gray-800">体重記録</p>
				<p class="mt-0.5 text-xs text-gray-500">日々の体重・体脂肪率を記録</p>
			</div>
			<svg class="ml-auto h-4 w-4 flex-shrink-0 text-gray-300 transition-colors group-hover:text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
				<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
			</svg>
		</a>

		<a
			href="/workout/exercise"
			class="group flex items-center gap-4 rounded-2xl border border-orange-100 bg-white p-5 shadow-sm transition-all hover:border-orange-200 hover:shadow-md"
		>
			<div
				class="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-orange-400 to-rose-500 shadow-md shadow-orange-500/20 transition-transform group-hover:scale-105"
			>
				<svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
					<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7M15 5l-6 7 6 7" />
				</svg>
			</div>
			<div class="min-w-0">
				<p class="text-sm font-semibold text-gray-800">種目マスタ</p>
				<p class="mt-0.5 text-xs text-gray-500">トレーニング種目の登録・管理</p>
			</div>
			<svg class="ml-auto h-4 w-4 flex-shrink-0 text-gray-300 transition-colors group-hover:text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
				<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
			</svg>
		</a>

		<a
			href="/workout/log"
			class="group flex items-center gap-4 rounded-2xl border border-orange-100 bg-white p-5 shadow-sm transition-all hover:border-orange-200 hover:shadow-md"
		>
			<div
				class="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-orange-400 to-rose-500 shadow-md shadow-orange-500/20 transition-transform group-hover:scale-105"
			>
				<svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
					<path stroke-linecap="round" stroke-linejoin="round" d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2M9 12h6M9 16h6M9 8h6" />
				</svg>
			</div>
			<div class="min-w-0">
				<p class="text-sm font-semibold text-gray-800">日々の記録</p>
				<p class="mt-0.5 text-xs text-gray-500">トレーニングのセット・回数を記録</p>
			</div>
			<svg class="ml-auto h-4 w-4 flex-shrink-0 text-gray-300 transition-colors group-hover:text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
				<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
			</svg>
		</a>

		<a
			href="/workout/calorie"
			class="group flex items-center gap-4 rounded-2xl border border-orange-100 bg-white p-5 shadow-sm transition-all hover:border-orange-200 hover:shadow-md"
		>
			<div
				class="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-xl bg-gradient-to-br from-orange-400 to-rose-500 shadow-md shadow-orange-500/20 transition-transform group-hover:scale-105"
			>
				<svg class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
					<path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
				</svg>
			</div>
			<div class="min-w-0">
				<p class="text-sm font-semibold text-gray-800">摂取カロリー記録</p>
				<p class="mt-0.5 text-xs text-gray-500">日々の摂取カロリーを記録</p>
			</div>
			<svg class="ml-auto h-4 w-4 flex-shrink-0 text-gray-300 transition-colors group-hover:text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
				<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
			</svg>
		</a>
	</div>
</div>
