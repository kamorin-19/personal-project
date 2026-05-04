# フロントエンド コーディング規約

## TypeScript / Svelte

- `strict: true`、`any` 型禁止
- 状態管理: Svelte 5 Runes (`$state`, `$derived`, `$effect`)。Svelte 4 store は使わない
- Tailwind v4: `tailwind.config.js` は存在しない。カスタマイズは `app.css` の `@theme {}` で行う
- 環境変数: ブラウザ公開変数は `PUBLIC_` プレフィックス必須。`$env/static/public` からインポート
- `default export` は使わない（named export のみ）
- コンポーネント命名: ファイル名・コンポーネント名ともに `PascalCase`（例: `WorkoutCard.svelte`）

## テスト（Vitest）

- テストファイルは `frontend/src/tests/` に配置し、`*.test.ts` で命名する

## コマンド

```bash
npm run generate:api  # OpenAPI → TypeScript SDK 生成
```

## API連携アーキテクチャ

- **開発時 (Docker)**: `vite.config.ts` の proxy が `/api/*` を `http://backend:8000` に転送
- **開発時 (ローカル)**: `BACKEND_HOST` 未設定時は `localhost:8000` に転送
- **本番時**: `PUBLIC_API_URL` 環境変数でエンドポイントを切り替え
- **型安全**: `@hey-api/openapi-ts` で Pydantic モデルから TypeScript SDK を自動生成
- `src/lib/api/client.ts` の `apiFetch<T>()` が基本 fetch ラッパー

## 注意事項

- `src/lib/api/generated/` は自動生成ファイル。手動編集禁止
- OpenAPI SDK 再生成: バックエンドの Pydantic モデル・エンドポイント変更後に `python export_openapi.py` → `npm run generate:api` を順に実行すること
