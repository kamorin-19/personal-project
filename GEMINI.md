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
    ├── gemini_to_claude/    # Gemini CLI → Claude Code 出力ファイル
    └── gemini_to_codex/     # Gemini CLI → Codex CLI 指示ファイル（簡易リファクタ委任）
```

## Gemini CLIへの出力ルール

### ファイルパス
- **必ず絶対パスを使用する**（相対パス禁止）
- 作業ディレクトリ: `c:/personal-project`

| 出力先 | パス | 用途 |
|---|---|---|
| Claude Code への報告（常時） | `c:/personal-project/interface/gemini_to_claude/{yyyymmdd}/{yyyymmdd}-{index}.md` | 全タスクの返却 |
| Codex CLI への委任（簡易リファクタのみ） | `c:/personal-project/interface/gemini_to_codex/{yyyymmdd}/{yyyymmdd}-{index}.md` | Codex向け指示テンプレート形式で出力 |

### 出力形式
- **200行以内**のMarkdown形式（厳守）
- 超過する場合は要点を絞って圧縮すること
- 出力完了後はファイルパスのみを返す（内容は返さない）

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

### index管理
同日・同出力先ディレクトリ内の `{yyyymmdd}-*.md` の最大index + 1 でインクリメントする。

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

### gemini-refactoring（リファクタリングアセスメント）
- コードベース全体から改善箇所を特定し難易度を判定する
- `--all-files` を使用してコードベース全体を解析
- 難易度判定基準:
  - **簡易**: 変更ファイル ≤3・新規ロジックなし・セキュリティ/DB/APIスキーマに無関係
  - **複雑**: 変更ファイル ≥4・ロジック変更あり・セキュリティ/DB/APIスキーマ関係・複数領域横断
- 簡易の場合: `gemini_to_codex/` に Codex向け指示テンプレート形式で実装指示を出力 → Codex が `codex_to_claude/` に完了報告を出力するまで待機 → 確認後 `gemini_to_claude/` に COMPLETE で報告（OUTPUT_FILES に codex_to_claude のパスを含める）
- 複雑の場合: `gemini_to_claude/` に NEEDS_REVIEW で報告

## 指示ファイルテンプレート（受け取り形式）

`claude_to_gemini/` への指示ファイルは以下の構造で記述される。

```md
## 調査テーマ
## 前提
## 知りたいこと
## 出力形式
```

## コーディング規約参照

各領域の規約ファイルに準拠すること。

| 領域 | 参照先 |
|---|---|
| フロントエンド | `frontend/CLAUDE.md` |
| バックエンド | `backend/CLAUDE.md` |
| インフラ・横断設定 | `docs/common.md` |

## 注意事項
- `.env` ファイルは読み込まない・出力に含めない
- `src/lib/api/generated/` は自動生成ファイルのため編集不可
- `node_modules/` は変更不可
