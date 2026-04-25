import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';
import Page from './+page.svelte';
import type { ExerciseResponse, WorkoutLogResponse } from '$lib/api/generated/types.gen';

const TEST_USER = { userId: 'user-001', email: 'test@example.com', name: 'Test User' };
const BASE_DATA = { user: TEST_USER, exercises: [] as ExerciseResponse[], logs: [] as WorkoutLogResponse[] };

describe('日々の記録ページ', () => {
	it('ページ見出しが表示される', () => {
		render(Page);
		expect(screen.getByRole('heading', { name: '日々の記録' })).toBeInTheDocument();
	});

	it('パンくずに「筋トレ」リンクが表示される', () => {
		render(Page);
		const link = screen.getByRole('link', { name: '筋トレ' });
		expect(link).toHaveAttribute('href', '/workout');
	});

	it('日付入力フィールドが存在する', () => {
		render(Page);
		const input = screen.getByLabelText('日付');
		expect(input).toBeInTheDocument();
		expect(input).toHaveAttribute('type', 'date');
		expect(input).toHaveAttribute('name', 'record_date');
	});

	it('重量入力フィールドが存在する', () => {
		render(Page);
		const input = screen.getByLabelText('重量');
		expect(input).toBeInTheDocument();
		expect(input).toHaveAttribute('type', 'number');
		expect(input).toHaveAttribute('max', '999');
		expect(input).toHaveAttribute('step', '0.5');
		expect(input).toHaveAttribute('name', 'weight_kg');
	});

	it('重量フィールドに kg 単位が表示される', () => {
		render(Page);
		expect(screen.getByText('kg')).toBeInTheDocument();
	});

	it('セット別回数のラベルが表示される', () => {
		render(Page);
		expect(screen.getByText('セット別回数')).toBeInTheDocument();
	});

	it('10セット分の入力フィールドが存在する', () => {
		render(Page);
		for (let i = 1; i <= 10; i++) {
			const input = screen.getByLabelText(`セット${i}`);
			expect(input).toBeInTheDocument();
			expect(input).toHaveAttribute('type', 'number');
			expect(input).toHaveAttribute('name', `set_${i}`);
		}
	});

	it('登録ボタンが存在する', () => {
		render(Page);
		const button = screen.getByRole('button', { name: '登録' });
		expect(button).toBeInTheDocument();
		expect(button).toHaveAttribute('type', 'submit');
	});

	it('クリアボタンが存在する', () => {
		render(Page);
		const button = screen.getByRole('button', { name: 'クリア' });
		expect(button).toBeInTheDocument();
		expect(button).toHaveAttribute('type', 'reset');
	});

	it('種目が未登録のとき案内メッセージが表示される', () => {
		render(Page, { props: { data: BASE_DATA, form: null } });
		expect(screen.getByText(/種目が登録されていません/)).toBeInTheDocument();
	});

	it('種目が未登録のとき種目マスタへのリンクが表示される', () => {
		render(Page, { props: { data: BASE_DATA, form: null } });
		const link = screen.getByRole('link', { name: '種目マスタ' });
		expect(link).toHaveAttribute('href', '/workout/exercise');
	});

	it('種目が登録されているとき選択セレクトが表示される', () => {
		const exercises: ExerciseResponse[] = [
			{
				exercise_id: 'ex-001',
				name: 'ベンチプレス',
				muscle_group: 'chest',
				calories_per_rep_per_kg: null,
				created_at: '2026-04-25T00:00:00+00:00',
				updated_at: '2026-04-25T00:00:00+00:00'
			}
		];
		render(Page, { props: { data: { ...BASE_DATA, exercises }, form: null } });
		expect(screen.getByRole('combobox')).toBeInTheDocument();
		expect(screen.getByRole('option', { name: 'ベンチプレス' })).toBeInTheDocument();
	});

	it('種目が部位ごとにグループ表示される', () => {
		const exercises: ExerciseResponse[] = [
			{
				exercise_id: 'ex-001',
				name: 'ベンチプレス',
				muscle_group: 'chest',
				calories_per_rep_per_kg: null,
				created_at: '2026-04-25T00:00:00+00:00',
				updated_at: '2026-04-25T00:00:00+00:00'
			},
			{
				exercise_id: 'ex-002',
				name: 'スクワット',
				muscle_group: 'leg',
				calories_per_rep_per_kg: null,
				created_at: '2026-04-25T00:00:00+00:00',
				updated_at: '2026-04-25T00:00:00+00:00'
			}
		];
		render(Page, { props: { data: { ...BASE_DATA, exercises }, form: null } });
		expect(screen.getByRole('option', { name: 'ベンチプレス' })).toBeInTheDocument();
		expect(screen.getByRole('option', { name: 'スクワット' })).toBeInTheDocument();
	});

	it('記録一覧が表示される', () => {
		const logs: WorkoutLogResponse[] = [
			{
				log_id: 'log-001',
				record_date: '2026-04-25',
				exercise_id: 'ex-001',
				exercise_name: 'ベンチプレス',
				weight_kg: 80,
				sets: [10, 8, 6],
				created_at: '2026-04-25T00:00:00+00:00',
				updated_at: '2026-04-25T00:00:00+00:00'
			}
		];
		render(Page, { props: { data: { ...BASE_DATA, logs }, form: null } });
		expect(screen.getByText('ベンチプレス')).toBeInTheDocument();
		expect(screen.getByText('2026-04-25')).toBeInTheDocument();
		expect(screen.getByText('80 kg')).toBeInTheDocument();
	});

	it('記録がないとき一覧セクションは表示されない', () => {
		render(Page, { props: { data: BASE_DATA, form: null } });
		expect(screen.queryByRole('heading', { name: '記録一覧' })).not.toBeInTheDocument();
	});

	it('記録に削除ボタンが存在する', () => {
		const logs: WorkoutLogResponse[] = [
			{
				log_id: 'log-001',
				record_date: '2026-04-25',
				exercise_id: 'ex-001',
				exercise_name: 'ベンチプレス',
				weight_kg: null,
				sets: [15, 12],
				created_at: '2026-04-25T00:00:00+00:00',
				updated_at: '2026-04-25T00:00:00+00:00'
			}
		];
		render(Page, { props: { data: { ...BASE_DATA, logs }, form: null } });
		const deleteBtn = screen.getByRole('button', { name: '削除' });
		expect(deleteBtn).toBeInTheDocument();
		expect(deleteBtn).toHaveAttribute('type', 'submit');
	});

	it('エラーメッセージが表示される', () => {
		render(Page, { props: { data: BASE_DATA, form: { error: '登録に失敗しました' } } });
		expect(screen.getByRole('alert')).toBeInTheDocument();
		expect(screen.getByText('登録に失敗しました')).toBeInTheDocument();
	});

	it('成功メッセージが表示される', () => {
		render(Page, { props: { data: BASE_DATA, form: { success: true } } });
		expect(screen.getByRole('status')).toBeInTheDocument();
		expect(screen.getByText('登録しました')).toBeInTheDocument();
	});
});
