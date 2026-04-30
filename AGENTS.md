# AGENTS.md — Codex CLI Project Configuration

このファイルはCodex CLIが自動読み込みするプロジェクト設定です。

## プロジェクト概要

筋トレ・競馬収支・予算を管理する個人向けWebアプリ。
マルチエージェント構成: Claude Code（オーケストレーション・実装）、Codex CLI（設計・テスト）、Gemini CLI（調査・レビュー）。

## 技術スタック

| レイヤー | 技術 |
|---|---|
| フロントエンド | SvelteKit 2 + Svelte 5 (Runes) + TypeScript strict |
| スタイリング | Tailwind CSS v4 |
| バックエンド | Python FastAPI |
| DB | DynamoDB |
| テスト (FE) | Vitest |
| テスト (BE) | pytest |

## ディレクトリ構成（重要箇所）

```
c:/personal-project/
├── frontend/src/
│   ├── routes/         # SvelteKit ページ
│   ├── lib/api/        # FastAPI連携クライアント
│   └── tests/          # Vitest テスト (*.test.ts)
├── backend/
│   ├── app/main.py
│   └── tests/          # pytest テスト (test_*.py)
└── interface/
    ├── claude_to_codex/   # Claude Code → Codex CLI 指示ファイル
    └── codex_to_claude/   # Codex CLI → Claude Code 出力ファイル
```

## Codex CLIへの出力ルール

### ファイルパス
- **必ず絶対パスを使用する**（相対パス禁止）
- 作業ディレクトリ: `c:/personal-project`
- 出力先: `c:/personal-project/interface/codex_to_claude/{yyyymmdd}/{yyyymmdd}-{index}.md`

### 出力形式
- **200行以内**のMarkdown形式（厳守）
- 超過する場合は要点を絞って圧縮すること
- 出力完了後はファイルパスのみを返す（内容は返さない）

### index管理
- 同日に複数回実行する場合、既存ファイル数+1でインクリメント
- 例: 既存ファイルが2件なら index=3

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

### テスト
- フロントエンド: `frontend/src/tests/` に `*.test.ts` で配置（Vitest）
- バックエンド: `backend/tests/` に `test_*.py` で配置（pytest）

## 注意事項
- `.env` ファイルは読み込まない・参照しない
- `src/lib/api/generated/` は自動生成ファイルのため編集不可
- `node_modules/` は変更不可
