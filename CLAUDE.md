# CLAUDE.md

筋トレ・競馬収支・予算を管理する個人向けWebアプリ。

## 技術スタック

| レイヤー | 技術 |
|---|---|
| フロントエンド | SvelteKit 2 + Svelte 5 (Runes) + TypeScript strict |
| バックエンド | Python FastAPI |
| DB | DynamoDB |
| インフラ | AWS / Docker Compose |

コーディング規約: `frontend/CLAUDE.md` / `backend/CLAUDE.md` を参照

## 重要な禁止事項

- `.env` はコミットしない
- `src/lib/api/generated/` は手動編集禁止（自動生成）
- Claude Code 自身はWeb検索不可 → `gemini-web-research` に委任すること

---

## ワークフロー選択

プロンプトに以下のタグを含めてください。Claude は対応ファイルを読み込んで進めます。

| タグ | 対応ファイル | 概要 |
|---|---|---|
| `[新規開発]` `[機能追加]` | `docs/workflow-feature.md` | フロー1（フルパイプライン） |
| `[機能修正]` | `docs/workflow-fix.md` | ファストパス or フロー1 |
| `[リファクタリング]` | `docs/workflow-refactor.md` | フロー3（難易度判定→分岐） |
| `[ドキュメント化]` | `docs/workflow-docs.md` | フロー2（Gemini生成） |

エージェント設定・ファイル連携ルール・レート制限対応: `docs/common.md` を参照
