# 種目マスタ リファクタリング テスト設計書

## テスト対象機能
1. load() の serverApiFetch() への切り替え
2. create アクション：エラーハンドリング（parseFloat失敗含む）
3. delete アクション：404エラー許容確認
4. +page.svelte の MUSCLE_GROUPS 定数化による表示一致

## テストケース

### 正常系
- ✅ ページ見出し「種目マスタ」が表示される
- ✅ 種目一覧が正しく表示される（muscleGroupLabel対応）
- ✅ 登録フォーム全フィールドが存在する
- ✅ クリアボタンがリセット機能を持つ

### 異常系
- ✅ parseFloat()失敗時のNaN処理：null として送信
- ✅ 削除時 404エラー：成功と同等扱い
- ✅ 認証なし：401エラー返却

### 境界値
- ✅ calories_per_rep_per_kg: 0（最小値）
- ✅ calories_per_rep_per_kg: 999.999（大値）
- ✅ 空文字列の値ミスマッチ検査なし

## テストデータ
- 部位ラベル 7種類：chest, back, shoulder, arm, abdomen, leg, other
- サンプル種目：{exercise_id: 1, name: "ベンチプレス", muscle_group: "chest", calories_per_rep_per_kg: 0.05}

## 注意点・前提条件
- 既存テスト exercise.test.ts はすべて通過必須
- バックエンド仕様に依存（エンドポイント変更時に修正対象）
- クライアント側の変更のみ。バックエンド応答形式変更なし
