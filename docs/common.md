# 共通設定

## エージェント役割

| エージェント | 役割 |
|---|---|
| Claude Code | overviewキャッシュ参照・大枠設計・レビュー対応・最終判断・ユーザー対話 |
| Codex CLI | 詳細設計・テスト設計・実装・テスト実装・修正ループ・次工程への引き継ぎ |
| Gemini CLI | コード全体把握・リファクタリング難易度判断・コードレビュー・Web調査・ドキュメント作成 |

## エージェント使い分け

| エージェント | 使うべきケース |
|---|---|
| Claude Code | 大枠設計・方針決定・トレードオフ判断・最終品質確認 |
| Codex CLI | 詳細設計・テスト設計・CRUD実装・テスト追加・型修正・軽微バグ修正・簡易リファクタ実装 |
| Gemini CLI | リファクタリング難易度判断・最新仕様確認・ライブラリ比較・Web調査・ドキュメント生成 |

## サブエージェント一覧

| サブエージェント | 用途 |
|---|---|
| `codex-design` | 大枠設計をもとに詳細設計書・テスト設計書を作成・codex-test-impl への引き継ぎ |
| `codex-test-impl` | 詳細設計書・テスト設計書をもとに実装・テスト実装・修正ループ・完了報告 |
| `gemini-code-overview` | コードベース全体把握 |
| `gemini-refactoring` | リファクタリング難易度判断・簡易リファクタの Codex 委任 |
| `gemini-code-review` | コードレビュー |
| `gemini-web-research` | Web調査・情報収集 |
| `gemini-docs` | ドキュメント作成 |

## overview キャッシュルール

キャッシュ優先原則: `docs/overview-*.md` が存在する場合、必ずキャッシュを先に確認。ファイル探索禁止。

| ファイル | 対象領域 |
|---|---|
| `overview-frontend.md` | SvelteKit構成・コンポーネント・ルーティング・API連携 |
| `overview-backend.md` | FastAPI構成・エンドポイント・Pydanticモデル・DynamoDB操作 |
| `overview-infra.md` | Docker・docker-compose・AWS構成・環境変数 |

## コンテキスト管理ルール

- **1タスク完了後は必ず `/clear` を実行してから次のタスクを受け付けること**
- タスク継続に必要な情報はすべて `docs/overview-*.md` または `interface/` 以下に書き出してからクリアすること
- `--resume` による前セッションの引き継ぎは原則禁止。再開が必要な場合は該当ファイルを読み込んで新セッションで起動すること

## レート制限対応ルール

**Claude Code がレート制限に達した場合:**
- 即時中断し、進捗状況を `interface/` または `docs/` に記録してから待機
- 再開時は記録ファイルを読み込んで中断箇所から再スタート

**Codex CLI がレート制限に達した場合:**
- `codex_to_claude/` に STATUS: RATE_LIMITED で報告
- 1回目: 30分待機後に再委任
- 2回連続: その日の追加タスクを中止してユーザーに報告

## ファイル連携ルール

- パス形式: `interface/{フォルダ名}/{yyyymmdd}/{yyyymmdd}-{index}.md`
- 連携ファイルは 200行以内（`docs/overview-*.md` は除く）
- 関連ファイルの絶対パスをサブエージェントへの指示に必ず明示すること
- 連携ファイルは要点のみ。冗長な表現は省くこと

### 連携フォルダと受け取り先

| 出力先 | 結果受け取り先 |
|---|---|
| `claude_to_gemini/` | `gemini_to_claude/` |
| `claude_to_codex/` | `codex_to_claude/`（完了報告）または `codex_to_codex/`（工程間引き継ぎ） |
| `gemini_to_codex/` | `codex_to_claude/` |

### Claude Code への入力制約

- 1依頼あたり 150行以内
- diff は要点のみ（全文貼り付け禁止）
- 実行ログは末尾 50行以内

### 返却ファイルフォーマット

```md
## STATUS
COMPLETE / ERROR / NEEDS_REVIEW / RATE_LIMITED のいずれか

## SUMMARY
3行以内で結果を要約

## OUTPUT_FILES
生成・変更したファイルの絶対パス一覧のみ

## ISSUES
（STATUS が ERROR または NEEDS_REVIEW の場合のみ）問題点を箇条書き
```

### 指示ファイルテンプレート

- Codex向け: `AGENTS.md` を参照
- Gemini向け: `GEMINI.md` を参照

## インフラ構成（Docker / AWS）

- **開発環境**: `docker compose up`（localhost:5173）、停止: `docker compose down`
- **Docker 内 proxy target**: `http://backend:8000`
- **ローカル開発**: `BACKEND_HOST` 環境変数で `http://localhost:8000` に切り替え
- **本番**: `PUBLIC_API_URL` 環境変数でエンドポイント切り替え
- **ボリューム**: `node_modules` は Docker 匿名ボリューム。ホスト側は使用しない
- **ホットリロード**: `usePolling: true` は WSL2/Linux 環境安定化のため常時有効

### 重要ファイル

- `docker-compose.yml` - frontend + backend 接続設定
- `Dockerfile` / `Dockerfile.dev` - コンテナイメージ定義
- `vite.config.ts` - Tailwind プラグイン + /api プロキシ設定
- `openapi-ts.config.ts` - OpenAPI SDK 自動生成設定
