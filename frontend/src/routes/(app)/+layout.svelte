<script lang="ts">
	import type { Snippet } from 'svelte';
	import { page } from '$app/state';
	import type { LayoutData } from './$types';

	let { children, data }: { children: Snippet; data: LayoutData } = $props();

	const navItems = [
		{ href: '/workout', label: '筋トレ' },
		{ href: '/keiba', label: '競馬' },
		{ href: '/budget', label: '予算' }
	] as const;

	const initials = $derived(
		((data.user.name ?? data.user.email) || '?').slice(0, 1).toUpperCase()
	);

	const isActive = $derived((href: string) => {
		if (href === '/') return page.url.pathname === '/';
		return page.url.pathname === href || page.url.pathname.startsWith(href + '/');
	});
</script>

<div class="min-h-screen bg-gray-50">
	<!-- スキップリンク -->
	<a
		href="#main-content"
		class="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-indigo-600 focus:px-4 focus:py-2 focus:text-sm focus:font-medium focus:text-white"
	>
		メインコンテンツへスキップ
	</a>

	<!-- モバイル用ヘッダー (lg以上では非表示) -->
	<header
		class="fixed top-0 z-30 flex h-14 w-full items-center justify-between border-b border-gray-200 bg-white px-4 lg:hidden"
	>
		<a href="/" class="flex items-center gap-2">
			<div
				class="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600"
			>
				<svg
					class="h-4 w-4 text-white"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					stroke-width="2"
					aria-hidden="true"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"
					/>
				</svg>
			</div>
			<span class="text-sm font-semibold text-gray-800">Personal Manager</span>
		</a>
		<div
			class="flex h-8 w-8 items-center justify-center rounded-full bg-indigo-600 text-xs font-bold text-white"
			aria-hidden="true"
		>
			{initials}
		</div>
	</header>

	<!-- デスクトップ用サイドバー (lg以上のみ表示) -->
	<aside
		class="fixed inset-y-0 left-0 hidden w-72 flex-col border-r border-gray-200 bg-white lg:flex"
	>
		<!-- ロゴ -->
		<div class="flex h-16 items-center gap-3 border-b border-gray-100 px-6">
			<div
				class="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 shadow-md shadow-indigo-500/20"
			>
				<svg
					class="h-5 w-5 text-white"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					stroke-width="1.8"
					aria-hidden="true"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"
					/>
				</svg>
			</div>
			<span class="font-semibold text-gray-800">Personal Manager</span>
		</div>

		<!-- ナビゲーション -->
		<nav class="flex-1 space-y-1 px-3 py-4" aria-label="メインナビゲーション">
			<a
				href="/"
				aria-current={isActive('/') ? 'page' : undefined}
				class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 {isActive(
					'/'
				)
					? 'bg-indigo-50 text-indigo-700'
					: 'text-gray-600 hover:bg-gray-100 hover:text-gray-800'}"
			>
				<svg
					class="h-5 w-5"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
					stroke-width="2"
					aria-hidden="true"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"
					/>
				</svg>
				ホーム
			</a>

			{#each navItems as item}
				<a
					href={item.href}
					aria-current={isActive(item.href) ? 'page' : undefined}
					class="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 {isActive(
						item.href
					)
						? 'bg-indigo-50 text-indigo-700'
						: 'text-gray-600 hover:bg-gray-100 hover:text-gray-800'}"
				>
					{#if item.href === '/workout'}
						<svg
							class="h-5 w-5"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
							aria-hidden="true"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M22 12h-4l-3 9L9 3l-3 9H2"
							/>
						</svg>
					{:else if item.href === '/keiba'}
						<svg
							class="h-5 w-5"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
							aria-hidden="true"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941"
							/>
						</svg>
					{:else if item.href === '/budget'}
						<svg
							class="h-5 w-5"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
							aria-hidden="true"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M21 12V7H5a2 2 0 0 1-2-2c0-1.1.9-2 2-2h14v4M3 5v14a2 2 0 0 0 2 2h16v-5M18 12a2 2 0 0 0 0 4h4v-4z"
							/>
						</svg>
					{/if}
					{item.label}
				</a>
			{/each}
		</nav>

		<!-- ユーザー情報 + ログアウト -->
		<div class="border-t border-gray-100 p-4">
			<div class="flex items-center gap-3">
				<div
					class="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-full bg-indigo-600 text-sm font-bold text-white"
					aria-hidden="true"
				>
					{initials}
				</div>
				<div class="min-w-0 flex-1">
					<p class="truncate text-sm font-medium text-gray-800">
						{data.user.name ?? 'ユーザー'}
					</p>
					<p class="truncate text-xs text-gray-500">{data.user.email}</p>
				</div>
				<form method="POST" action="/logout">
					<button
						type="submit"
						title="ログアウト"
						class="flex h-8 w-8 items-center justify-center rounded-lg text-gray-400 transition-colors hover:bg-gray-100 hover:text-gray-600 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
					>
						<svg
							class="h-4 w-4"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
							aria-hidden="true"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75"
							/>
						</svg>
						<span class="sr-only">ログアウト</span>
					</button>
				</form>
			</div>
		</div>
	</aside>

	<!-- メインコンテンツ -->
	<main id="main-content" class="pt-14 pb-16 lg:ml-72 lg:pt-0 lg:pb-0">
		{@render children()}
	</main>

	<!-- モバイル用ボトムナビ (lg以上では非表示) -->
	<nav
		class="fixed bottom-0 z-30 flex h-16 w-full items-stretch border-t border-gray-200 bg-white lg:hidden"
		aria-label="メインナビゲーション（モバイル）"
	>
		<a
			href="/"
			aria-current={isActive('/') ? 'page' : undefined}
			class="flex flex-1 flex-col items-center justify-center gap-0.5 text-xs font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 {isActive(
				'/'
			)
				? 'text-indigo-600'
				: 'text-gray-400'}"
		>
			<svg
				class="h-5 w-5"
				fill="none"
				viewBox="0 0 24 24"
				stroke="currentColor"
				stroke-width="2"
				aria-hidden="true"
			>
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h8.25"
				/>
			</svg>
			ホーム
		</a>

		{#each navItems as item}
			<a
				href={item.href}
				aria-current={isActive(item.href) ? 'page' : undefined}
				class="flex flex-1 flex-col items-center justify-center gap-0.5 text-xs font-medium transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500 {isActive(
					item.href
				)
					? 'text-indigo-600'
					: 'text-gray-400'}"
			>
				{#if item.href === '/workout'}
					<svg
						class="h-5 w-5"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
						aria-hidden="true"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M22 12h-4l-3 9L9 3l-3 9H2"
						/>
					</svg>
				{:else if item.href === '/keiba'}
					<svg
						class="h-5 w-5"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
						aria-hidden="true"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941"
						/>
					</svg>
				{:else if item.href === '/budget'}
					<svg
						class="h-5 w-5"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
						aria-hidden="true"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M21 12V7H5a2 2 0 0 1-2-2c0-1.1.9-2 2-2h14v4M3 5v14a2 2 0 0 0 2 2h16v-5M18 12a2 2 0 0 0 0 4h4v-4z"
						/>
					</svg>
				{/if}
				{item.label}
			</a>
		{/each}
	</nav>
</div>
