import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';
import Page from './+page.svelte';

describe('種目マスタページ', () => {
	it('ページ見出しが表示される', () => {
		render(Page);
		expect(screen.getByRole('heading', { name: '種目マスタ' })).toBeInTheDocument();
	});

	it('パンくずに「筋トレ」リンクが表示される', () => {
		render(Page);
		const link = screen.getByRole('link', { name: '筋トレ' });
		expect(link).toHaveAttribute('href', '/workout');
	});

	it('種目名入力フィールドが存在する', () => {
		render(Page);
		const input = screen.getByLabelText('種目名');
		expect(input).toBeInTheDocument();
		expect(input).toHaveAttribute('type', 'text');
	});

	it('部位セレクトボックスが存在する', () => {
		render(Page);
		const select = screen.getByLabelText('部位');
		expect(select).toBeInTheDocument();
	});

	it('部位セレクトに全7部位の選択肢がある', () => {
		render(Page);
		expect(screen.getByRole('option', { name: '胸' })).toBeInTheDocument();
		expect(screen.getByRole('option', { name: '背中' })).toBeInTheDocument();
		expect(screen.getByRole('option', { name: '肩' })).toBeInTheDocument();
		expect(screen.getByRole('option', { name: '腕' })).toBeInTheDocument();
		expect(screen.getByRole('option', { name: '腹' })).toBeInTheDocument();
		expect(screen.getByRole('option', { name: '脚' })).toBeInTheDocument();
		expect(screen.getByRole('option', { name: 'その他' })).toBeInTheDocument();
	});

	it('推定消費カロリー入力フィールドが存在する', () => {
		render(Page);
		const input = screen.getByLabelText(/推定消費カロリー/);
		expect(input).toBeInTheDocument();
		expect(input).toHaveAttribute('type', 'number');
		expect(input).toHaveAttribute('step', '0.001');
		expect(input).toHaveAttribute('min', '0');
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
});
