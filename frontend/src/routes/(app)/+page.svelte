<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	const greeting = $derived((() => {
		const hour = new Date().getHours();
		if (hour < 12) return 'おはようございます';
		if (hour < 18) return 'こんにちは';
		return 'こんばんは';
	})());

	const features = [
		{
			href: '/workout',
			label: '筋トレ',
			description: 'トレーニング記録・メニュー管理',
			color: 'from-orange-400 to-rose-500',
			bg: 'bg-orange-50',
			border: 'border-orange-100'
		},
		{
			href: '/keiba',
			label: '競馬収支',
			description: '馬券の収支・投資履歴を管理',
			color: 'from-emerald-400 to-teal-500',
			bg: 'bg-emerald-50',
			border: 'border-emerald-100'
		},
		{
			href: '/budget',
			label: '予算管理',
			description: '月次予算・支出のトラッキング',
			color: 'from-indigo-400 to-violet-500',
			bg: 'bg-indigo-50',
			border: 'border-indigo-100'
		}
	] as const;
</script>

<svelte:head>
	<title>ホーム — Personal Manager</title>
</svelte:head>

<div class="px-4 py-6 lg:px-8 lg:py-10">
	<!-- グリーティング -->
	<div class="mb-8">
		<p class="text-sm text-gray-500">{greeting}、</p>
		<h1 class="mt-0.5 text-2xl font-bold text-gray-900">
			{data.user.name ?? data.user.email} さん
		</h1>
	</div>

	<!-- 機能カード -->
	<section>
		<h2 class="mb-4 text-xs font-semibold uppercase tracking-wider text-gray-400">機能</h2>
		<div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
			{#each features as feature}
				<a
					href={feature.href}
					class="group relative overflow-hidden rounded-2xl border {feature.border} {feature.bg} p-5 transition-all hover:shadow-md"
				>
					<!-- グラデーションアイコン -->
					<div
						class="mb-4 inline-flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br {feature.color} shadow-md"
					>
						{#if feature.href === '/workout'}
							<svg
								class="h-6 w-6 text-white"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
								stroke-width="2"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									d="M22 12h-4l-3 9L9 3l-3 9H2"
								/>
							</svg>
						{:else if feature.href === '/keiba'}
							<svg
								class="h-6 w-6 text-white"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
								stroke-width="2"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941"
								/>
							</svg>
						{:else if feature.href === '/budget'}
							<svg
								class="h-6 w-6 text-white"
								fill="none"
								viewBox="0 0 24 24"
								stroke="currentColor"
								stroke-width="2"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									d="M21 12V7H5a2 2 0 0 1-2-2c0-1.1.9-2 2-2h14v4M3 5v14a2 2 0 0 0 2 2h16v-5M18 12a2 2 0 0 0 0 4h4v-4z"
								/>
							</svg>
						{/if}
					</div>

					<h3 class="font-semibold text-gray-800">{feature.label}</h3>
					<p class="mt-1 text-sm text-gray-500">{feature.description}</p>

					<!-- 近日公開バッジ -->
					<span
						class="mt-3 inline-block rounded-full bg-white/70 px-2.5 py-0.5 text-xs font-medium text-gray-500"
					>
						近日公開
					</span>

					<!-- ホバー矢印 -->
					<div
						class="absolute right-4 top-1/2 -translate-y-1/2 opacity-0 transition-opacity group-hover:opacity-100"
					>
						<svg
							class="h-5 w-5 text-gray-400"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M8.25 4.5l7.5 7.5-7.5 7.5"
							/>
						</svg>
					</div>
				</a>
			{/each}
		</div>
	</section>
</div>
