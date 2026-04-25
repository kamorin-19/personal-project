import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';
import Page from './+page.svelte';
import type { CalorieLogResponse } from '$lib/api/generated/types.gen';

const TEST_USER = { userId: 'user-001', email: 'test@example.com', name: 'Test User' };
const BASE_DATA = { user: TEST_USER, records: [] as CalorieLogResponse[] };

describe('摂取カロリー記録ページ', () => {
	it('ページ見出しが表示される', () => {
		render(Page);
		expect(screen.getByRole('heading', { name: '摂取カロリー記録' })).toBeInTheDocument();
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

	it('摂取カロリー入力フィールドが存在する', () => {
		render(Page);
		const input = screen.getByLabelText('摂取カロリー');
		expect(input).toBeInTheDocument();
		expect(input).toHaveAttribute('type', 'number');
		expect(input).toHaveAttribute('min', '0');
		expect(input).toHaveAttribute('max', '99999');
		expect(input).toHaveAttribute('step', '1');
		expect(input).toHaveAttribute('name', 'calories');
	});

	it('kcal 単位が表示される', () => {
		render(Page);
		expect(screen.getByText('kcal')).toBeInTheDocument();
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

	it('記録がないとき一覧セクションは表示されない', () => {
		render(Page, { props: { data: BASE_DATA, form: null } });
		expect(screen.queryByText('記録一覧')).not.toBeInTheDocument();
	});

	it('記録一覧が表示される', () => {
		const records: CalorieLogResponse[] = [
			{
				record_date: '2026-04-25',
				calories: 2000,
				created_at: '2026-04-25T00:00:00+00:00',
				updated_at: '2026-04-25T00:00:00+00:00'
			}
		];
		render(Page, { props: { data: { ...BASE_DATA, records }, form: null } });
		expect(screen.getByText('2026-04-25')).toBeInTheDocument();
		expect(screen.getByText(/2,000 kcal|2000 kcal/)).toBeInTheDocument();
	});

	it('記録に削除ボタンが存在する', () => {
		const records: CalorieLogResponse[] = [
			{
				record_date: '2026-04-25',
				calories: 1800,
				created_at: '2026-04-25T00:00:00+00:00',
				updated_at: '2026-04-25T00:00:00+00:00'
			}
		];
		render(Page, { props: { data: { ...BASE_DATA, records }, form: null } });
		const btn = screen.getByRole('button', { name: /削除/ });
		expect(btn).toBeInTheDocument();
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
