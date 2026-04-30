# GEMINI.md — Gemini CLI Project Configuration

このファイルはGemini CLIが自動読み込みするプロジェクト設定です。

## プロジェクト概要

筋トレ・競馬収支・予算を管理する個人向けWebアプリ。
マルチエージェント構成: Claude Code（大枠設計・オーケストレーション）、Codex CLI（詳細設計・テスト設計・実装）、Gemini CLI（コード把握・レビュー・調査・ドキュメント）。

## 技術スタック

| レイヤー | 技術 |
|---|---|
| フロントエンド | SvelteKit 2 + Svelte 5 (Runes) + TypeScript strict |
| スタイリング | Tailwind CSS v4 |
| バックエンド | Python FastAPI |
| DB | DynamoDB |
| テスト (FE) | Vitest (`frontend/src/tests/*.test.ts`) |
| テスト (BE) | pytest (`backend/tests/test_*.py`) |

## ディレクトリ構成（重要箇所）

```
c:/personal-project/
├── frontend/src/
│   ├── routes/              # SvelteKit ページ (+page.svelte, +layout.svelte)
│   ├── lib/
│   │   ├── api/client.ts    # fetch ラッパー apiFetch<T>()
│   │   ├── api/generated/   # 自動生成SDK（編集禁止）
│   │   └── components/      # 共通UIコンポーネント
│   └── tests/               # Vitest テスト
├── backend/
│   ├── app/main.py
│   └── tests/               # pytest テスト
└── interface/
    ├── claude_to_gemini/    # Claude Code → Gemini CLI 指示ファイル
    └── gemini_to_claude/    # Gemini CLI → Claude Code 出力ファイル
```

## Gemini CLIへの出力ルール

### ファイルパス
- **必ず絶対パスを使用する**（相対パス禁止）
- 作業ディレクトリ: `c:/personal-project`
- 出力先: `c:/personal-project/interface/gemini_to_claude/{yyyymmdd}/{yyyymmdd}-{index}.md`

### 出力形式
- **200行以内**のMarkdown形式（厳守）
- 超過する場合は要点を絞って圧縮すること
- 出力完了後はファイルパスのみを返す（内容は返さない）

### index管理
- 同日に複数回実行する場合、既存ファイル数+1でインクリメント

### --all-files の使用方針
- コードベース全体が必要な場合（レビュー・全体把握）: `--all-files` を使用
- Web調査のみの場合: `--all-files` を使用しない
- `.env` や秘密情報は出力に含めない

## 役割別タスク

### gemini-code-overview（コードベース全体把握）
- アーキテクチャ・依存関係・影響範囲の調査
- `--all-files` を使用してコードベース全体を解析

### gemini-code-review（コードレビュー）
- 品質・可読性・バグ・セキュリティ・規約準拠を確認
- 指摘事項は重要度（高/中/低）付きで出力

### gemini-web-research（Web調査）
- 技術情報・ライブラリ・ベストプラクティスの調査
- `--all-files` は使用しない

### gemini-docs（ドキュメント作成）
- API仕様書・設計書・READMEなどの生成
- 読み手を意識した構成・表現で作成

## コーディング規約

### フロントエンド (TypeScript / Svelte)
- `strict: true`、`any` 型禁止
- Svelte 5 Runes (`$state`, `$derived`, `$effect`) を使用、Svelte 4 store は使わない
- `default export` は使わない（named export のみ）
- コンポーネント名・ファイル名は PascalCase

### バックエンド (Python / FastAPI)
- PEP 8 準拠
- 全関数引数・戻り値に型ヒント必須
- 変数・関数は snake_case、クラスは PascalCase
- リクエスト/レスポンスは Pydantic モデルで定義

## 注意事項
- `.env` ファイルは読み込まない・出力に含めない
- `src/lib/api/generated/` は自動生成ファイルのため編集不可
- `node_modules/` は変更不可
