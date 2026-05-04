# AGENTS.md — Codex CLI Project Configuration

Codex CLIが自動読み込みするプロジェクト設定。

## 役割

Codex CLIは詳細設計・テスト設計・実装を担当する。Claude Codeが作成した大枠設計書を受け取り、codex-designが詳細設計書・テスト設計書を一括作成→codex-test-implが実装・テスト通過まで自律的に引き継ぐ。

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

Claude Codeが大枠設計書（`docs/design-{yyyymmdd}-{index}.md`、40行以内）を作成し、Codex CLIが詳細設計書に拡充する。

**大枠設計書（受け取り時の形式）:**

```md
## 目的
## 変更対象ファイル
## インターフェース定義
## 実装方針
## 制約
```

**詳細設計書（codex-designが大枠設計書の末尾に追記するセクション）・テスト設計書（codex-designが docs/ に新規作成）:**

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
    ├── gemini_to_codex/     # 入力（Gemini CLIからの指示・簡易リファクタ委任）
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
COMPLETE / ERROR / NEEDS_REVIEW / RATE_LIMITED のいずれか

## SUMMARY
3行以内で結果を要約

## OUTPUT_FILES
生成・変更したファイルの絶対パス一覧のみ

## ISSUES
（STATUS が ERROR の場合のみ）問題点を箇条書きで記載
```

## コーディング規約

## コーディング規約参照

詳細は各領域の CLAUDE.md を参照すること。

| 領域 | 参照先 |
|---|---|
| フロントエンド | `frontend/CLAUDE.md` |
| バックエンド | `backend/CLAUDE.md` |

## 指示ファイルテンプレート（受け取り形式）

`claude_to_codex/`、`codex_to_codex/`、`gemini_to_codex/` への指示ファイルは以下の構造で記述される。

```md
## 目的
## 対象ファイル
## 制約
## 実装内容
## テスト要否
## 次工程
（該当する場合のみ）次に実行するサブエージェント名と引き継ぎ先パスを記載
```

## 禁止事項
- `.env` ファイルは読み込まない・参照しない
- `src/lib/api/generated/` は編集不可（自動生成）
- `node_modules/` は変更不可