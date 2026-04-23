<script lang="ts">
	import { enhance } from '$app/forms';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>ログイン — Personal Manager</title>
</svelte:head>

<div class="relative flex min-h-screen items-center justify-center overflow-hidden bg-[#080b14]">
	<!-- 背景デコレーション -->
	<div class="pointer-events-none absolute inset-0" aria-hidden="true">
		<div
			class="absolute -left-40 -top-40 h-[600px] w-[600px] rounded-full bg-indigo-600/20 blur-[120px]"
		></div>
		<div
			class="absolute -bottom-40 -right-40 h-[500px] w-[500px] rounded-full bg-violet-600/20 blur-[120px]"
		></div>
		<div
			class="absolute left-1/2 top-1/2 h-[300px] w-[300px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-blue-500/10 blur-[80px]"
		></div>
		<div
			class="absolute inset-0 opacity-[0.03]"
			style="background-image: linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px); background-size: 48px 48px;"
		></div>
	</div>

	<!-- カード -->
	<div class="relative z-10 w-full max-w-md px-4">
		<div class="rounded-3xl border border-white/10 bg-white/[0.05] p-10 shadow-2xl backdrop-blur-2xl">
			<!-- ロゴ & タイトル -->
			<div class="mb-10 text-center">
				<div
					class="mb-5 inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-600 shadow-lg shadow-indigo-500/30"
				>
					<svg
						class="h-8 w-8 text-white"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="1.8"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"
						/>
					</svg>
				</div>
				<h1 class="text-2xl font-bold tracking-tight text-white">Personal Manager</h1>
				<p class="mt-2 text-sm text-white/40">筋トレ・競馬・予算を、一画面で。</p>
			</div>

			<!-- Google ログインボタン -->
			<form method="POST" action="?/googleLogin" use:enhance>
				<button
					type="submit"
					class="group relative flex w-full items-center justify-center gap-3 overflow-hidden rounded-2xl bg-white px-6 py-3.5 text-sm font-semibold text-gray-800 shadow-lg transition-all duration-200 hover:shadow-xl hover:shadow-white/10 active:scale-[0.98]"
				>
					<svg class="h-5 w-5 flex-shrink-0" viewBox="0 0 24 24" aria-hidden="true">
						<path
							d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
							fill="#4285F4"
						/>
						<path
							d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
							fill="#34A853"
						/>
						<path
							d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
							fill="#FBBC05"
						/>
						<path
							d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
							fill="#EA4335"
						/>
					</svg>
					<span>Google でログイン</span>
					<span
						class="absolute inset-0 -translate-x-full bg-gradient-to-r from-transparent via-white/10 to-transparent transition-transform duration-500 group-hover:translate-x-full"
					></span>
				</button>
			</form>

			<!-- 開発環境バイパス -->
			{#if data.dev}
				<div class="mt-6">
					<div class="relative flex items-center gap-3">
						<div class="h-px flex-1 bg-white/10"></div>
						<span class="text-xs text-white/20">DEV</span>
						<div class="h-px flex-1 bg-white/10"></div>
					</div>
					<form method="POST" action="?/devLogin" use:enhance class="mt-4">
						<button
							type="submit"
							class="flex w-full items-center justify-center gap-2 rounded-xl border border-amber-500/30 bg-amber-500/10 px-6 py-3 text-sm font-medium text-amber-400 transition-colors hover:bg-amber-500/20"
						>
							<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 12H3m18 0h-1.5m-15 3.75H3m18 0h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 002.25-2.25V6.75a2.25 2.25 0 00-2.25-2.25H6.75A2.25 2.25 0 004.5 6.75v10.5a2.25 2.25 0 002.25 2.25zm.75-12h9v9h-9v-9z" />
							</svg>
							開発用ログイン (認証スキップ)
						</button>
					</form>
				</div>
			{/if}

			<!-- フッター -->
			<p class="mt-8 text-center text-xs text-white/25">
				ログインすることで、サービスの利用規約と<br />プライバシーポリシーに同意したものとみなします。
			</p>
		</div>
	</div>
</div>
