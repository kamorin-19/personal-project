# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# プロジェクト概要

筋トレ・競馬収支・予算を管理する個人向けWebアプリ。

## 技術スタック

| レイヤー | 技術 |
|---|---|
| フロントエンド | SvelteKit 2 + Svelte 5 (Runes) + TypeScript strict |
| スタイリング | Tailwind CSS v4 (CSS-first、config不要) |
| バックエンド | Python FastAPI |
| DB | DynamoDB |
| インフラ | AWS |
| コンテナ | Docker / Docker Compose |

---

## ディレクトリ構成

```
personal-project/
├── frontend/               # SvelteKit アプリ
│   ├── src/
│   │   ├── routes/         # ページ (+page.svelte, +layout.svelte)
│   │   ├── lib/
│   │   │   ├── api/        # FastAPI連携クライアント
│   │   │   │   ├── client.ts        # fetch ラッパー apiFetch<T>()
│   │   │   │   └── generated/       # openapi-ts 自動生成 SDK (手動編集禁止)
│   │   │   └── components/ # 共通UIコンポーネント
│   │   ├── app.html
│   │   └── app.css         # Tailwind v4 エントリ (@import "tailwindcss")
│   ├── Dockerfile           # 本番用マルチステージビルド
│   ├── Dockerfile.dev       # 開発用 (ホットリロード対応)
│   ├── vite.config.ts      # Tailwind プラグイン + /api プロキシ設定
│   ├── svelte.config.js
│   ├── openapi-ts.config.ts
│   └── .env.example
├── backend/                # FastAPI アプリ (未作成)
│   ├── app/main.py
│   └── openapi.json        # npm run generate:api の入力源
├── docker-compose.yml      # frontend + backend を接続
└── interface/              # Gemini調査結果の共有ディレクトリ
    └── {yyyymmdd}/
        └── gemini-cli-{index}.md
```

---

## よく使うコマンド

### Docker (推奨)

```bash
# 開発環境起動 (localhost:5173)
docker compose up

# 再ビルドして起動
docker compose up --build

# バックグラウンド起動
docker compose up -d

# 停止
docker compose down
```

### ローカル直接実行 (frontend/ ディレクトリで)

```bash
npm run dev        # 開発サーバー起動
npm run build      # ビルド
npm run check      # 型チェック
npm run lint       # ESLint
npm run format     # Prettier
npm run generate:api  # FastAPI OpenAPI スキーマから TypeScript SDK を生成
```

**FastAPI の OpenAPI スキーマ書き出し (backend側)**
```bash
cd backend && python export_openapi.py   # backend/openapi.json を生成
```

---

## API連携アーキテクチャ

- **開発時 (Docker)**: `vite.config.ts` の proxy が `/api/*` を `http://backend:8000` (サービス名) に転送
- **開発時 (ローカル)**: `BACKEND_HOST` 未設定時は `localhost:8000` に転送
- **本番時**: `PUBLIC_API_URL` 環境変数でエンドポイントを切り替え
- **型安全**: `@hey-api/openapi-ts` で Pydantic モデルから TypeScript SDK を自動生成
- `src/lib/api/client.ts` の `apiFetch<T>()` が基本 fetch ラッパー

---

## コーディング規約

- **TypeScript**: `strict: true`、`any` 型禁止
- **状態管理**: Svelte 5 Runes (`$state`, `$derived`, `$effect`)。Svelte 4 store は使わない
- **Tailwind v4**: `tailwind.config.js` は存在しない。カスタマイズは `app.css` の `@theme {}` で行う
- **環境変数**: ブラウザ公開変数は `PUBLIC_` プレフィックス必須。`$env/static/public` からインポート
- **named export**: `default export` は使わない

---

## 重要な注意事項

- **`.env` はコミットしない**。`.env.example` を参照
- **`src/lib/api/generated/`** は自動生成ファイル。手動編集禁止
- **`node_modules` ボリューム**: Docker Compose では匿名ボリュームでコンテナ内を保護。ホスト側の `node_modules` は使用しない
- **Vite proxy の target**: Docker 内は `http://backend:8000`、ローカルは `http://localhost:8000`。`BACKEND_HOST` 環境変数で切り替え
- **`usePolling: true`**: WSL2/Linux 環境でのホットリロード安定化のため常時有効
- Webの検索を行う場合は必ず`gemini-research` サブエージェントに調査を依頼し、調査内容を受け取ること、Claude CodeでのWeb検索は絶対に行わないこと

---

## 作業ワークフロー

1. **Claude Code**: オーケストレーション・設計・実装を担当
2. **Gemini CLI** (`gemini-review` サブエージェント): レビュー・ドキュメント作成を担当
3. **Gemini CLI** (`gemini-research` サブエージェント): Web調査担当
4. Gemini の調査結果は `interface/` ディレクトリ以下にMarkdownで保存されるので、そのファイルの内容をコンテキストとして利用する

## ファイル連携注意事項
./personal-project/interface/$(date +%Y%m%d)/でGemini CLIの調査結果を連携する、このルールを破らないこと。
