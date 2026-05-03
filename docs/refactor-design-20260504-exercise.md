# 種目マスタ リファクタリング 詳細設計書

## 目的
APIクライアント側の DRY 化、エラーハンドリング改善、型安全性向上による保守性向上

## 対象ファイル
- `c:\personal-project\frontend\src\routes\(app)\workout\exercise\+page.server.ts`
- `c:\personal-project\frontend\src\routes\(app)\workout\exercise\+page.svelte`
- `c:\personal-project\frontend\src\routes\(app)\workout\exercise\exercise.test.ts`（テスト確認のみ）

## インターフェース定義

### +page.server.ts (リファクタリング後)

```typescript
// 変更内容:
// 1. backendUrl(), authHeaders() をローカル定義から削除
// 2. serverApiFetch<T>() を $lib/api/client.ts から import して使用
// 3. エラーハンドリング: try/catch で統一、parseFloat()失敗時のNaN処理追加
// 4. 404エラーは削除成功と同等とみなす（既存ロジック継続）
```

### +page.svelte (リファクタリング後)

```typescript
// 変更内容:
// 1. muscleGroupLabel を const MUSCLE_GROUPS で定数化
// 2. delete フォーム enhance を完全実装（update呼び出し追加）
// 3. error/success の重複確認コード削除（既存のif分岐は保持）
```

## 実装方針
- serverApiFetch()の既存実装を活用、新規実装なし
- テスト互換性を保証（exercise.test.ts の実行結果に変化なし）
- エラーメッセージの日本語/API応答を区別

## 採用しなかった選択肢と理由
- コンポーネント化（error/success表示）：フロントエンドの小規模機能のため見送り
- muscle_group型定義拡張：バックエンド仕様確認不足のため見送り

## 依存関係・注意事項
- $lib/api/client.ts の serverApiFetch()の動作が前提
- バックエンド /workout/exercise エンドポイントの仕様に依存
- 既存テスト exercise.test.ts との互換性確保必須
