<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();

	// デフォルト: 直近30日
	const today = new Date();
	const thirtyDaysAgo = new Date(today);
	thirtyDaysAgo.setDate(today.getDate() - 29);

	function toDateStr(d: Date): string {
		return d.toISOString().slice(0, 10);
	}

	let fromDate = $state(toDateStr(thirtyDaysAgo));
	let toDate = $state(toDateStr(today));

	// --- モックデータ生成 ---
	function generateDateRange(from: string, to: string): string[] {
		const dates: string[] = [];
		const cur = new Date(from);
		const end = new Date(to);
		while (cur <= end) {
			dates.push(toDateStr(cur));
			cur.setDate(cur.getDate() + 1);
		}
		return dates;
	}

	const MOCK_BASE = '2026-03-28';
	const MOCK_DAYS = 30;

	function mockWeights(): Record<string, number> {
		const result: Record<string, number> = {};
		let w = 72.8;
		for (let i = 0; i < MOCK_DAYS; i++) {
			const d = new Date(MOCK_BASE);
			d.setDate(d.getDate() + i);
			const str = toDateStr(d);
			w += (Math.random() - 0.52) * 0.3;
			result[str] = Math.round(w * 10) / 10;
		}
		return result;
	}

	function mockCaloriesIn(): Record<string, number> {
		const result: Record<string, number> = {};
		for (let i = 0; i < MOCK_DAYS; i++) {
			const d = new Date(MOCK_BASE);
			d.setDate(d.getDate() + i);
			result[toDateStr(d)] = 1600 + Math.floor(Math.random() * 900);
		}
		return result;
	}

	function mockCaloriesBurned(): Record<string, number> {
		const result: Record<string, number> = {};
		for (let i = 0; i < MOCK_DAYS; i++) {
			const d = new Date(MOCK_BASE);
			d.setDate(d.getDate() + i);
			// 週2〜3日はトレーニングあり
			result[toDateStr(d)] = i % 3 === 0 ? 0 : 250 + Math.floor(Math.random() * 350);
		}
		return result;
	}

	const WEIGHT_DATA = mockWeights();
	const CALORIE_IN_DATA = mockCaloriesIn();
	const CALORIE_BURNED_DATA = mockCaloriesBurned();

	// --- チャート用データ抽出 ---
	let chartDates = $derived(generateDateRange(fromDate, toDate));
	let weightValues = $derived(chartDates.map((d) => WEIGHT_DATA[d] ?? null));
	let calorieInValues = $derived(chartDates.map((d) => CALORIE_IN_DATA[d] ?? null));
	let calorieBurnedValues = $derived(chartDates.map((d) => CALORIE_BURNED_DATA[d] ?? null));

	// --- Canvas refs ---
	let weightCanvas: HTMLCanvasElement | undefined = $state();
	let intakeCanvas: HTMLCanvasElement | undefined = $state();
	let burnedCanvas: HTMLCanvasElement | undefined = $state();

	// --- Chart instances ---
	let weightChart: import('chart.js').Chart | undefined;
	let intakeChart: import('chart.js').Chart | undefined;
	let burnedChart: import('chart.js').Chart | undefined;

	const CHART_DEFAULTS = {
		responsive: true,
		maintainAspectRatio: false,
		plugins: {
			legend: { display: false },
			tooltip: { mode: 'index' as const, intersect: false }
		},
		scales: {
			x: {
				grid: { color: 'rgba(0,0,0,0.05)' },
				ticks: { maxTicksLimit: 8, font: { size: 11 } }
			},
			y: {
				grid: { color: 'rgba(0,0,0,0.05)' },
				ticks: { font: { size: 11 } }
			}
		}
	};

	async function initCharts() {
		const { Chart, registerables } = await import('chart.js');
		Chart.register(...registerables);

		weightChart?.destroy();
		intakeChart?.destroy();
		burnedChart?.destroy();

		const labels = chartDates;

		if (weightCanvas) {
			weightChart = new Chart(weightCanvas, {
				type: 'line',
				data: {
					labels,
					datasets: [
						{
							data: weightValues,
							borderColor: '#f97316',
							backgroundColor: 'rgba(249,115,22,0.08)',
							borderWidth: 2,
							pointRadius: 3,
							pointBackgroundColor: '#f97316',
							tension: 0.3,
							fill: true,
							spanGaps: true
						}
					]
				},
				options: {
					...CHART_DEFAULTS,
					scales: {
						...CHART_DEFAULTS.scales,
						y: {
							...CHART_DEFAULTS.scales.y,
							title: { display: true, text: 'kg', font: { size: 11 } }
						}
					}
				}
			});
		}

		if (intakeCanvas) {
			intakeChart = new Chart(intakeCanvas, {
				type: 'bar',
				data: {
					labels,
					datasets: [
						{
							data: calorieInValues,
							backgroundColor: 'rgba(59,130,246,0.7)',
							borderColor: '#3b82f6',
							borderWidth: 1,
							borderRadius: 4
						}
					]
				},
				options: {
					...CHART_DEFAULTS,
					scales: {
						...CHART_DEFAULTS.scales,
						y: {
							...CHART_DEFAULTS.scales.y,
							title: { display: true, text: 'kcal', font: { size: 11 } }
						}
					}
				}
			});
		}

		if (burnedCanvas) {
			burnedChart = new Chart(burnedCanvas, {
				type: 'bar',
				data: {
					labels,
					datasets: [
						{
							data: calorieBurnedValues,
							backgroundColor: 'rgba(34,197,94,0.7)',
							borderColor: '#22c55e',
							borderWidth: 1,
							borderRadius: 4
						}
					]
				},
				options: {
					...CHART_DEFAULTS,
					scales: {
						...CHART_DEFAULTS.scales,
						y: {
							...CHART_DEFAULTS.scales.y,
							title: { display: true, text: 'kcal', font: { size: 11 } }
						}
					}
				}
			});
		}
	}

	$effect(() => {
		if (weightCanvas && intakeCanvas && burnedCanvas) {
			initCharts();
		}
		return () => {
			weightChart?.destroy();
			intakeChart?.destroy();
			burnedChart?.destroy();
		};
	});

	function onSearch() {
		initCharts();
	}
</script>

<svelte:head>
	<title>グラフ表示 — Personal Manager</title>
</svelte:head>

<div class="px-4 py-6 lg:px-8 lg:py-10">
	<!-- パンくず -->
	<nav class="mb-6 flex items-center gap-2 text-sm text-gray-500" aria-label="パンくずリスト">
		<a href="/workout" class="hover:text-gray-700">筋トレ</a>
		<svg class="h-4 w-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
			<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
		</svg>
		<span class="font-medium text-gray-800" aria-current="page">グラフ表示</span>
	</nav>

	<div class="mb-6">
		<h1 class="text-2xl font-bold text-gray-900">グラフ表示</h1>
		<p class="mt-1 text-sm text-gray-500">体重・摂取カロリー・消費カロリーの推移を確認できます</p>
	</div>

	<!-- 日付範囲フィルター -->
	<div class="mb-8 rounded-2xl border border-gray-200 bg-white p-4 shadow-sm sm:p-5">
		<div class="flex flex-wrap items-end gap-4">
			<div>
				<label for="from-date" class="block text-xs font-medium text-gray-600">開始日</label>
				<input
					id="from-date"
					type="date"
					bind:value={fromDate}
					class="mt-1 block rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-sm focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
				/>
			</div>
			<div>
				<label for="to-date" class="block text-xs font-medium text-gray-600">終了日</label>
				<input
					id="to-date"
					type="date"
					bind:value={toDate}
					class="mt-1 block rounded-xl border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 shadow-sm focus:border-orange-400 focus:outline-none focus:ring-2 focus:ring-orange-400/20"
				/>
			</div>
			<button
				onclick={onSearch}
				class="rounded-xl bg-gradient-to-r from-orange-400 to-rose-500 px-5 py-2 text-sm font-semibold text-white shadow-sm shadow-orange-500/20 transition-all hover:from-orange-500 hover:to-rose-600 hover:shadow-md active:scale-[0.98]"
			>
				表示
			</button>
		</div>
	</div>

	<!-- チャート -->
	<div class="space-y-6">
		<!-- 体重 -->
		<div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
			<div class="mb-4 flex items-center gap-2">
				<span class="flex h-7 w-7 items-center justify-center rounded-lg bg-orange-100">
					<svg class="h-4 w-4 text-orange-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
						<path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
					</svg>
				</span>
				<div>
					<p class="text-sm font-semibold text-gray-800">体重</p>
					<p class="text-xs text-gray-400">単位: kg</p>
				</div>
			</div>
			<div class="h-52 sm:h-64">
				<canvas bind:this={weightCanvas}></canvas>
			</div>
		</div>

		<!-- 摂取カロリー -->
		<div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
			<div class="mb-4 flex items-center gap-2">
				<span class="flex h-7 w-7 items-center justify-center rounded-lg bg-blue-100">
					<svg class="h-4 w-4 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
						<path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
					</svg>
				</span>
				<div>
					<p class="text-sm font-semibold text-gray-800">摂取カロリー</p>
					<p class="text-xs text-gray-400">単位: kcal</p>
				</div>
			</div>
			<div class="h-52 sm:h-64">
				<canvas bind:this={intakeCanvas}></canvas>
			</div>
		</div>

		<!-- 消費カロリー -->
		<div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
			<div class="mb-4 flex items-center gap-2">
				<span class="flex h-7 w-7 items-center justify-center rounded-lg bg-green-100">
					<svg class="h-4 w-4 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true">
						<path stroke-linecap="round" stroke-linejoin="round" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z" />
						<path stroke-linecap="round" stroke-linejoin="round" d="M9.879 16.121A3 3 0 1012.015 11L11 14H9c0 .768.293 1.536.879 2.121z" />
					</svg>
				</span>
				<div>
					<p class="text-sm font-semibold text-gray-800">消費カロリー</p>
					<p class="text-xs text-gray-400">単位: kcal（トレーニングによる推定消費）</p>
				</div>
			</div>
			<div class="h-52 sm:h-64">
				<canvas bind:this={burnedCanvas}></canvas>
			</div>
		</div>
	</div>
</div>
