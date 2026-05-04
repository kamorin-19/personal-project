# ワークフロー: [リファクタリング]

フロー3を適用する。

## フロー

```
① overview キャッシュ確認（docs/overview-*.md）
   └→ claude_to_gemini/ に難易度判断指示（gemini-refactoring）

② 難易度判定（Gemini）
   - ファイル数・新規ロジック・セキュリティ/DB/APIスキーマ関係を総合評価

③-A 簡易判定 → Codex 委任
   └→ gemini_to_codex/ に実装指示 → codex-test-impl 起動
      ↓
      Codex が codex_to_claude/ に完了報告を出力
      ↓
      Gemini が codex_to_claude/ の完了を確認
      ↓
      gemini_to_claude/ に STATUS: COMPLETE で報告 → /clear

③-B 複雑判定 → フロー1 へ移行
   └→ gemini_to_claude/ で NEEDS_REVIEW 報告 → docs/workflow-feature.md を参照 → /clear
```

## 難易度判定基準

| 簡易（Codex 委任） | 複雑（フロー1 へ移行） |
|---|---|
| ファイル ≤3・新規ロジックなし・セキュリティ/DB/APIスキーマ無関係 | ファイル ≥4・ロジック変更あり・セキュリティ/DB/API関係・複数領域横断 |

## 完了

`/clear` を実行してから次のタスクを受け付ける。
