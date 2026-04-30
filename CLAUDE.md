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
│   │   ├── tests/          # Vitest テストファイル (*.test.ts)
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
│   ├── tests/              # pytest テストファイル (test_*.py)
│   └── openapi.json        # npm run generate:api の入力源
├── docs/
│   ├── overview-frontend.md  # フロントエンド概要キャッシュ（300行以内・自動更新）
│   ├── overview-backend.md   # バックエンド概要キャッシュ（300行以内・自動更新）
│   ├── overview-infra.md     # インフラ概要キャッシュ（300行以内・自動更新）
│   └── {その他ドキュメント}   # gemini-docs が出力するドキュメント
├── docker-compose.yml      # frontend + backend を接続
└── interface/              # エージェント間ファイル連携ディレクトリ
    ├── claude_to_codex/    # Claude Code → Codex CLI への指示ファイル
    │   └── {yyyymmdd}/
    │       └── {yyyymmdd}-{index}.md
    ├── claude_to_gemini/   # Claude Code → Gemini CLI への指示ファイル
    │   └── {yyyymmdd}/
    │       └── {yyyymmdd}-{index}.md
    ├── codex_to_codex/     # Codex CLI → Codex CLI への引き継ぎファイル（パイプライン用）
    │   └── {yyyymmdd}/
    │       └── {yyyymmdd}-{index}.md
    ├── codex_to_claude/    # Codex CLI → Claude Code への返却ファイル
    │   └── {yyyymmdd}/
    │       └── {yyyymmdd}-{index}.md
    └── gemini_to_claude/   # Gemini CLI → Claude Code への返却ファイル
        └── {yyyymmdd}/
            └── {yyyymmdd}-{index}.md
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

### フロントエンド (TypeScript / Svelte)

- **TypeScript**: `strict: true`、`any` 型禁止
- **状態管理**: Svelte 5 Runes (`$state`, `$derived`, `$effect`)。Svelte 4 store は使わない
- **Tailwind v4**: `tailwind.config.js` は存在しない。カスタマイズは `app.css` の `@theme {}` で行う
- **環境変数**: ブラウザ公開変数は `PUBLIC_` プレフィックス必須。`$env/static/public` からインポート
- **named export**: `default export` は使わない
- **コンポーネント命名**: ファイル名・コンポーネント名ともに `PascalCase`（例: `WorkoutCard.svelte`）

### バックエンド (Python / FastAPI)

- **スタイル**: PEP 8 準拠
- **型ヒント**: すべての関数引数・戻り値に型ヒント必須
- **命名**: 変数・関数は `snake_case`、クラスは `PascalCase`
- **リクエスト/レスポンス**: Pydantic モデルで定義する
- **定数**: モジュールレベルに `UPPER_SNAKE_CASE` で定義する

### テスト

- **フロントエンド**: Vitest を使用。テストファイルは `frontend/src/tests/` に配置し、`*.test.ts` で命名する
- **バックエンド**: pytest を使用。テストファイルは `backend/tests/` に配置し、`test_*.py` で命名する

---

## 重要な注意事項

- **`.env` はコミットしない**。`.env.example` を参照
- **`src/lib/api/generated/`** は自動生成ファイル。手動編集禁止
- **OpenAPI SDK再生成**: バックエンドの Pydantic モデル・エンドポイントを変更したら必ず `python export_openapi.py` → `npm run generate:api` を順に実行すること
- **`node_modules` ボリューム**: Docker Compose では匿名ボリュームでコンテナ内を保護。ホスト側の `node_modules` は使用しない
- **Vite proxy の target**: Docker 内は `http://backend:8000`、ローカルは `http://localhost:8000`。`BACKEND_HOST` 環境変数で切り替え
- **`usePolling: true`**: WSL2/Linux 環境でのホットリロード安定化のため常時有効
- **Web検索禁止**: Claude Code は自身でWeb検索を行わないこと。Web調査が必要な場合は `gemini-web-research` サブエージェントに委任し、結果を `interface/gemini_to_claude/` 経由で受け取ること

---

## 作業ワークフロー

### エージェント役割

| エージェント | 役割 |
|---|---|
| Claude Code | overviewキャッシュ参照・大枠設計・レビュー対応・最終判断・ユーザー対話 |
| Codex CLI | 詳細設計・テスト設計・実装・テスト実装・修正ループ・次工程への引き継ぎ |
| Gemini CLI | コードの全体把握・コードレビュー・Web調査・ドキュメント作成 |

### エージェント使い分け判断基準

| エージェント | 使うべきケース |
|---|---|
| Claude Code | 大枠設計・方針決定・トレードオフ判断・最終品質確認 |
| Codex CLI | 詳細設計・テスト設計・CRUD実装・テスト追加・型修正・リファクタ・軽微バグ修正 |
| Gemini CLI | 最新仕様確認・ライブラリ比較・Web調査・ドキュメント生成・コードベース把握 |

---

### サブエージェント一覧

| サブエージェント | 用途 |
|---|---|
| `codex-design` | 大枠設計をもとに詳細設計書を作成・次工程（codex-test-design）への引き継ぎ指示生成 |
| `codex-test-design` | テスト設計書の作成・次工程（codex-impl）への引き継ぎ指示生成 |
| `codex-impl` | 詳細設計書をもとに実装・テスト実装・テスト通過までの修正ループ・Claude Code への完了報告 |
| `gemini-code-overview` | コードベース全体把握（領域別に実行） |
| `gemini-code-review` | コードレビュー |
| `gemini-web-research` | Web調査・情報収集 |
| `gemini-docs` | ドキュメント作成 |

---

### gemini-code-overview キャッシュルール

overviewキャッシュはフロントエンド・バックエンド・インフラの3ファイルに分割する。
タスクに関係する領域のファイルのみ参照・更新すること。**各ファイルは300行以内を目安とする。**

| キャッシュファイル | 対象領域 |
|---|---|
| `docs/overview-frontend.md` | SvelteKit構成・コンポーネント・ルーティング・API連携クライアント |
| `docs/overview-backend.md` | FastAPI構成・エンドポイント・Pydanticモデル・DynamoDB操作 |
| `docs/overview-infra.md` | Docker・docker-compose・AWS構成・環境変数 |

**参照ルール：** 対象キャッシュファイルが存在し、かつ直近の実装タスク以降に更新されている場合は `gemini-code-overview` を再実行しないこと。

**更新が必要なケース（該当領域のファイルのみ更新）：**
- 対象領域に新規ファイル・ディレクトリの追加があった
- 対象領域に複数ファイルにまたがる大規模な変更があった
- 前回のoverview生成から大幅に時間が経過した
- 対象キャッシュファイルが300行を超えた場合は `gemini-code-overview` を再実行して再要約・上書きすること。別ファイルへの分割は行わない

---

### コンテキスト管理ルール

Claude Code のコンテキスト汚染を防ぐため、以下のルールを必ず守ること。

- **1タスク完了後は必ず `/clear` を実行してから次のタスクを受け付けること**
- タスクの継続に必要な情報はすべて `docs/overview-*.md` または `interface/` 以下のファイルに書き出してからクリアすること
- `--resume` による前セッションの引き継ぎは原則禁止。再開が必要な場合は該当ファイルを読み込んで新セッションで起動すること

---

### レート制限対応ルール

Claude Code・Codex CLI はともに Pro プランのレート制限が存在する。
制限に達した場合は以下のルールで対処すること。

**Claude Code がレート制限に達した場合：**
- 作業を即時中断し、現在の進捗状況（完了済み手順・未完了手順・生成済みファイルパス）を `interface/codex_to_claude/` または `docs/` 以下のファイルに記録してから待機すること
- 再開時は記録ファイルを読み込んで中断箇所から再スタートすること（`--resume` は使わない）

**Codex CLI がレート制限に達した場合：**
- 作業を中断し、`codex_to_claude/` に以下の形式でレート制限報告を出力すること
- Claude Code は報告を受け取り、再試行のタイミングを判断すること

```md
## STATUS
RATE_LIMITED

## SUMMARY
レート制限に達したため作業を中断

## OUTPUT_FILES
中断時点までに生成・変更済みのファイルパス一覧

## ISSUES
中断した手順と、再開時に必要な情報を記載
```

---

### 設計書フォーマット（2段階）

設計書はClaude Codeが作成する**大枠設計書**と、codex-designが拡充する**詳細設計書**の2段階で構成する。

**ファイル命名規則（上書き防止のため必ず守ること）：**
- 大枠設計書（Claude Code出力）: `docs/design-{yyyymmdd}-{index}.md`
- テスト設計書: `docs/test-design-{yyyymmdd}-{index}.md`

#### 大枠設計書（Claude Code作成・30行以内）

```md
## 目的
変更・追加の目的を2〜3行で記載

## 変更対象ファイル
変更・新規作成するファイルの絶対パスを列挙

## インターフェース定義
関数シグネチャ・型定義・APIエンドポイントのみ記載（説明不要）
（変更がない場合は「変更なし」と記載）

## 実装方針
採用するアプローチを1〜2行で記載（採用しなかった選択肢の記載はcodex-designに委ねる）
```

#### 詳細設計書（codex-design が大枠設計書に追記・拡充）

codex-designは大枠設計書の内容を維持しつつ、以下を追記すること。

```md
## 採用しなかった選択肢と理由

## 依存関係・注意事項
他ファイル・他モジュールへの影響範囲、既存コードとの整合性で注意すべき点
```

---

### フロー1: プログラム実装

**Claude Code は overviewキャッシュ参照・大枠設計・レビュー対応を担当する。
詳細設計→テスト設計→実装の連鎖（手順3〜5）は各Codexエージェントが自律的に引き継ぐ。**

```
Claude Code
  │
  │ ① overviewキャッシュ確認・大枠設計書作成（30行以内）
  │   （docs/overview-*.md を参照。コードベースの直接参照は原則禁止）
  ▼
Claude Code ─────────────────────────────────── 大枠設計書を docs/ に出力
  │
  │ ② 詳細設計指示（claude_to_codex/）
  ▼
codex-design ───────────────────────────────── 詳細設計書を docs/ に出力
  │
  │ ③ 引き継ぎ（codex_to_codex/）
  ▼
codex-test-design ──────────────────────────── テスト設計書を docs/ に出力
  │
  │ ④ 引き継ぎ（codex_to_codex/）
  ▼
codex-impl ─────────────────────────────────── 実装・テスト修正ループ
  │
  │ ⑤ 完了報告（codex_to_claude/）
  ▼
Claude Code
  │
  │ ⑥ レビュー指示（claude_to_gemini/）※レビュー判定ルールに従い選択的に実行
  ▼
gemini-code-review
  │
  │ ⑦ レビュー結果（gemini_to_claude/）
  ▼
Claude Code ─── レビュー対応ルールに従い対処 → /clear
```

**手順詳細：**

1. **Claude Code：** タスクに関係する領域の `docs/overview-{領域}.md` を確認する。キャッシュルールに従い必要な場合のみ `gemini-code-overview` を実行して更新する。overviewキャッシュを参照して大枠設計書（**30行以内**）を作成し `docs/` に出力する（**コードベースの直接参照は原則禁止**。どうしても必要な場合は1ターンあたり最大2ファイルまで）
2. **Claude Code：** 大枠設計書のパスを添えて `codex-design` に詳細設計を指示する（`claude_to_codex/`）
3. **codex-design：** 大枠設計書をもとに詳細設計書を作成し `docs/` に出力する。完了後、詳細設計書のパスを添えて `codex-test-design` への引き継ぎ指示を `codex_to_codex/` に出力する
4. **codex-test-design：** テスト設計書を作成し `docs/` に出力する。完了後、詳細設計書・テスト設計書のパスを添えて `codex-impl` への引き継ぎ指示を `codex_to_codex/` に出力する
5. **codex-impl：** 詳細設計書・テスト設計書をもとに実装・テスト実装を行い、全テスト通過まで修正ループを回す。完了後、完了報告を `codex_to_claude/` に出力する
6. **Claude Code：** 完了報告の STATUS と SUMMARY を確認し、レビュー判定ルールに従い `gemini-code-review` へのレビュー指示を行う（`claude_to_gemini/`）
7. **Claude Code：** レビュー結果を受け取り、レビュー対応ルールに従い対処する。完了後 `/clear` を実行する

**エラー発生時（codex-impl が修正ループを抜けられない場合）：**
- 修正ループが3回を超えた場合は中断し、`codex_to_claude/` にエラー報告を出力すること
- Claude Code はエラー内容を確認し、設計を見直すか直接対処するかを判断する

**随時使用するサブエージェント（必須手順外）**

- `gemini-web-research`: 技術情報・ライブラリ調査が必要な場面で随時使用する
- `gemini-docs`: 実装完了後にドキュメント作成が必要な場合に使用する

---

### レビュー対応ルール

#### レビュー実行判定

フロー1手順6に進む前に、変更内容に応じてレビューを実行するか判定すること。

| 変更の種類 | レビュー要否 |
|---|---|
| UI文言・スタイルのみの変更 | スキップ可 |
| コンポーネント追加・ロジック変更 | スキップ可（変更が小規模な場合） |
| 認証・セキュリティ関連の変更 | **必須** |
| DB操作（DynamoDB）の変更 | **必須** |
| APIエンドポイント・スキーマの変更 | **必須** |

#### レビュー結果への対処

`gemini-code-review` の返却内容に応じて、以下のルールで対処すること。

| 指摘の種類 | 対処方法 |
|---|---|
| typo・命名・フォーマットのみ | Claude Code が直接修正する。フロー1手順6には戻らない |
| 設計変更・ロジック修正を伴う指摘 | `codex-impl` に修正を委任し、フロー1手順5から再実行する |

---

### フロー2: コード理解・ドキュメント化

**ドキュメント化タスクを受けたら、以下の順序で実行すること。手順の省略・順序の変更は禁止。**

1. `gemini-code-overview` にコードベースの概要把握を依頼し、結果を受け取る
2. 受け取った概要をもとに `gemini-docs` にドキュメント化を依頼する
   - 出力先は `docs/` ディレクトリを指定すること（`interface/` 以下には出力しない）
   - ファイル名は内容を表す名前にする（例: `docs/architecture.md`、`docs/api-overview.md`）
3. `gemini-docs` がドキュメントを `docs/` に出力し、出力ファイルの絶対パスを返却する
4. 返却されたファイルパスをユーザーに報告する。完了後 `/clear` を実行する

---

## ファイル連携注意事項

- 各連携フォルダのパスは `interface/{フォルダ名}/{yyyymmdd}/{yyyymmdd}-{index}.md` の形式とする。このルールを破らないこと。
- `claude_to_gemini/` への出力後、Gemini CLIの結果は `gemini_to_claude/` から受け取ること
- `claude_to_codex/` への出力後の結果は `codex_to_claude/`（最終完了報告）または `codex_to_codex/`（工程間引き継ぎ）から受け取ること
- 連携ファイルの内容は必ず200行以内に収めること（`docs/overview-*.md` は除く）。このルールは絶対に守ること
- 連携ファイルは内容を損なわない範囲で短いほどよい。不要な説明・冗長な表現は省き、要点のみを記載すること
- **関連ファイルパスを必ず明示すること**: サブエージェントへの指示ファイルには、タスクに関係するファイル・ディレクトリの絶対パスを記載する。これによりサブエージェントの余分な探索を防ぎ、精度とトークン効率を高める

### Claude Code への入力制約

Claude Code に渡す情報は以下の上限を守ること。これを超える場合は要約してから渡すこと。

- 1依頼あたり 150行以内
- diff は要点のみ（全文貼り付け禁止）
- 実行ログは末尾 50行以内

### Codex向け指示テンプレート

`claude_to_codex/` および `codex_to_codex/` への指示ファイルは以下の構造を使うこと。

```md
## 目的
## 対象ファイル
## 制約
## 実装内容
## テスト要否
## 次工程
（該当する場合のみ）次に実行するサブエージェント名と引き継ぎ先パスを記載
```

### codex-impl 実装制約

`codex-impl` への指示ファイルには `## 制約` セクションに以下を**必ず含めること**。

```md
## 制約
### 言語・フレームワーク制約
- フロントエンド: Svelte 5 Runes必須（$state / $derived / $effect を使うこと）
- フロントエンド: Svelte 4 store（writable / readable 等）は使用禁止
- フロントエンド: TypeScript strict準拠・any型禁止・named exportのみ
- フロントエンド: Tailwind v4（tailwind.config.js は存在しない。@theme{}でカスタマイズ）
- バックエンド: 型ヒント必須・PEP8準拠・Pydanticモデルでリクエスト/レスポンス定義

### テスト修正制約
- テスト通過のためにテストコード自体を変更することは禁止
- 修正は実装コードのみに限定すること
- 修正ループが3回を超えた場合は中断し codex_to_claude/ にエラー報告を出力すること
```

### Gemini向け指示テンプレート

`claude_to_gemini/` への指示ファイルは以下の構造を使うこと。

```md
## 調査テーマ
## 前提
## 知りたいこと
## 出力形式
```

### 返却ファイル必須フォーマット

各サブエージェントの返却ファイルは以下の構造を**必ず守ること**。Claude Code は STATUS と SUMMARY を確認して次のアクションを判断し、詳細が必要な場合のみ OUTPUT_FILES を参照すること。

```md
## STATUS
COMPLETE / ERROR / NEEDS_REVIEW / RATE_LIMITED のいずれか

## SUMMARY
3行以内で結果を要約

## OUTPUT_FILES
生成・変更したファイルの絶対パス一覧のみ

## ISSUES
（STATUS が ERROR または NEEDS_REVIEW の場合のみ記載）
問題点を箇条書きで記載
```
