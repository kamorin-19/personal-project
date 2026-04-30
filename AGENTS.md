# AGENTS.md — Codex CLI Project Configuration

Codex CLIが自動読み込みするプロジェクト設定。

## 役割

Codex CLIは詳細設計・テスト設計・実装を担当する。Claude Codeが作成した大枠設計書を受け取り、詳細設計書に拡充→テスト設計→実装・テスト通過まで自律的に引き継ぐ。

## 技術スタック

| レイヤー | 技術 |
|---|---|
| フロントエンド | SvelteKit 2 + Svelte 5 (Runes) + TypeScript strict |
| スタイリング | Tailwind CSS v4 |
| バックエンド | Python FastAPI |
| DB | DynamoDB |
| テスト (FE) | Vitest |
| テスト (BE) | pytest |

## 設計書フォーマット（2段階）

Claude Codeが大枠設計書（`docs/design-{yyyymmdd}-{index}.md`、30行以内）を作成し、Codex CLIが詳細設計書に拡充する。

**大枠設計書（受け取り時の形式）:**

```md
## 目的
## 変更対象ファイル
## インターフェース定義
## 実装方針
```

**詳細設計書（codex-designが大枠設計書の末尾に追記するセクション）:**

```md
## 採用しなかった選択肢と理由
## 依存関係・注意事項
```

## ディレクトリ構成

```
c:/personal-project/
├── docs/                    # 設計書・テスト設計書の出力先
├── frontend/src/
│   ├── routes/
│   ├── lib/api/generated/   # 編集禁止（自動生成）
│   └── tests/               # Vitest テスト
├── backend/
│   └── tests/               # pytest テスト
└── interface/
    ├── claude_to_codex/     # 入力（Claude Codeからの指示）
    ├── codex_to_codex/      # 工程間引き継ぎ
    └── codex_to_claude/     # 出力（Claude Codeへの完了報告）
```

## 出力ルール

### ファイルパス
- 必ず絶対パスを使用する（相対パス禁止）
- 作業ディレクトリ: `c:/personal-project`

### 出力先と形式

| 種別 | 出力先（絶対パス） | 形式 |
|---|---|---|
| 詳細設計書 | `c:/personal-project/docs/design-{yyyymmdd}-{index}.md` | 大枠設計書末尾に追記 |
| テスト設計書 | `c:/personal-project/docs/test-design-{yyyymmdd}-{index}.md` | 200行以内Markdown |
| 工程間引き継ぎ | `c:/personal-project/interface/codex_to_codex/{yyyymmdd}/{yyyymmdd}-{index}.md` | 200行以内Markdown |
| 完了報告 | `c:/personal-project/interface/codex_to_claude/{yyyymmdd}/{yyyymmdd}-{index}.md` | 下記フォーマット準拠 |

### index管理
同一日付・同一出力先ディレクトリ内の `{yyyymmdd}-*.md` の最大index + 1 でインクリメントする。

### 完了報告フォーマット（codex_to_claude/ のみ）

```md
## STATUS
COMPLETE / ERROR / RATE_LIMITED のいずれか

## SUMMARY
3行以内で結果を要約

## OUTPUT_FILES
生成・変更したファイルの絶対パス一覧のみ

## ISSUES
（STATUS が ERROR の場合のみ）問題点を箇条書きで記載
```

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
- フロントエンド: `c:/personal-project/frontend/src/tests/` に `*.test.ts` で配置（Vitest）
- バックエンド: `c:/personal-project/backend/tests/` に `test_*.py` で配置（pytest）

## 禁止事項
- `.env` ファイルは読み込まない・参照しない
- `src/lib/api/generated/` は編集不可（自動生成）
- `node_modules/` は変更不可