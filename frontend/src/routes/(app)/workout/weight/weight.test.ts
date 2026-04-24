import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';
import Page from './+page.svelte';

describe('体重記録ページ', () => {
	it('ページタイトルが表示される', () => {
		render(Page);
		expect(screen.getByRole('heading', { name: '体重記録' })).toBeInTheDocument();
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
	});

	it('体重入力フィールドが存在する', () => {
		render(Page);
		const input = screen.getByLabelText('体重');
		expect(input).toBeInTheDocument();
		expect(input).toHaveAttribute('type', 'number');
		expect(input).toHaveAttribute('max', '300');
		expect(input).toHaveAttribute('step', '0.1');
	});

	it('体脂肪率入力フィールドが存在する', () => {
		render(Page);
		const input = screen.getByLabelText('体脂肪率');
		expect(input).toBeInTheDocument();
		expect(input).toHaveAttribute('type', 'number');
		expect(input).toHaveAttribute('max', '100');
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

	it('体重フィールドに kg 単位が表示される', () => {
		render(Page);
		expect(screen.getByText('kg')).toBeInTheDocument();
	});

	it('体脂肪率フィールドに % 単位が表示される', () => {
		render(Page);
		expect(screen.getByText('%')).toBeInTheDocument();
	});
});
