# FastAPI Backend Overview

## ディレクトリ構成

```
backend/
├── app/
│   ├── main.py                 # FastAPI アプリ初期化・ルーター登録
│   ├── config.py               # Pydantic Settings（環境変数）
│   ├── dependencies.py         # 認証・DynamoDB依存性注入
│   ├── models/                 # （予約済み・未使用）
│   ├── schemas/                # Pydanticリクエスト/レスポンスモデル
│   │   ├── auth.py
│   │   ├── exercise.py
│   │   ├── weight.py
│   │   ├── workout_log.py
│   │   └── calorie_log.py
│   ├── repositories/           # DynamoDB操作（CRUD）
│   │   ├── exercise.py
│   │   ├── weight.py
│   │   ├── workout_log.py
│   │   └── calorie_log.py
│   └── routers/                # FastAPIエンドポイント定義
│       ├── auth.py
│       ├── exercise.py
│       ├── weight.py
│       ├── workout_log.py
│       └── calorie_log.py
├── tests/                      # pytest テストケース（1800行以上）
├── create_tables.py            # DynamoDB テーブル初期化スクリプト
├── export_openapi.py           # OpenAPI スキーマ出力
└── requirements.txt            # Python依存パッケージ
```

## エンドポイント一覧

### 認証系
- `POST /auth/google/callback` - Google OAuth2 コールバック → JWT トークン発行

### エクササイズ
- `POST /workout/exercise` - エクササイズマスター作成（*要認証）
- `GET /workout/exercise` - ユーザーのエクササイズ一覧取得（*要認証）
- `DELETE /workout/exercise/{exercise_id}` - エクササイズ削除（*要認証）

### 体重記録
- `POST /workout/weight` - 体重記録作成/更新（upsert、*要認証）
- `GET /workout/weight` - ユーザーの体重記録一覧取得（日付範囲フィルタ対応、*要認証）
- `DELETE /workout/weight/{record_date}` - 体重記録削除（*要認証）

### ワークアウトログ
- `POST /workout/log` - ワークアウトログ作成（*要認証）
- `GET /workout/log` - ワークアウトログ一覧取得（*要認証）
- `DELETE /workout/log/{log_id}` - ワークアウトログ削除（*要認証）

### カロリーログ
- `POST /workout/calorie-log` - カロリーログ作成（*要認証）
- `GET /workout/calorie-log` - カロリーログ一覧取得（日付範囲フィルタ対応、*要認証）
- `DELETE /workout/calorie-log/{log_id}` - カロリーログ削除（*要認証）

### その他
- `GET /health` - ヘルスチェック（認証不要）

## Pydancticモデル構造

### Exercise（エクササイズマスター）
```python
class ExerciseCreate:
    name: str                          # 1〜100文字
    muscle_group: MuscleGroup          # Enum: chest|back|shoulder|arm|abdomen|leg|other
    calories_per_rep_per_kg: float|None

class ExerciseResponse:
    exercise_id: str                   # UUID
    name: str
    muscle_group: MuscleGroup
    calories_per_rep_per_kg: float|None
    created_at: str                    # ISO 8601
    updated_at: str
    # from_dynamo()クラスメソッドで DynamoDB形式から変換
```

### Weight（体重記録）
```python
class WeightRecordCreate:
    record_date: str                   # YYYY-MM-DD形式（バリデーション付き）
    weight_kg: float                   # 0 < x <= 300
    body_fat_pct: float|None           # 0 <= x <= 100 (オプション)

class WeightRecordResponse:
    record_date: str
    weight_kg: float
    body_fat_pct: float|None
    created_at: str
    updated_at: str
```

### WorkoutLog（ワークアウトログ）
- exercise_id: 外部キー参照
- set_count: セット数
- rep_count: レップ数
- weight_kg: 使用重量
- logged_at: ISO 8601タイムスタンプ

### CalorieLog（カロリーログ）
- log_date: YYYY-MM-DD
- calories_intake: 摂取カロリー
- calories_burned: 消費カロリー
- notes: 備考（オプション）

## DynamoDB操作

### テーブル一覧（create_tables.py参照）
| テーブル名 | パーティションキー | ソートキー | GSI |
|---|---|---|---|
| users | userId | — | — |
| exercises | userId | exerciseId | — |
| weight | userId | recordDate | — |
| workout_logs | userId | loggedAt | — |
| calorie_logs | userId | logDate | — |

### Repository パターン
各Repository は以下のメソッドを提供：
- `create()` / `upsert()` - 作成・更新（PUTアイテム）
- `list_by_user()` - ユーザーのデータ取得（KeyConditionExpression で Query）
- `delete()` - 削除（ReturnValues="ALL_OLD"で存在確認）
- `get()` / `get_by_date_range()` - 範囲検索（Query + FilterExpression）

### DynamoDB接続
- aioboto3 + boto3.dynamodb.conditions を使用（async対応）
- エンドポイント: 環境変数 `DYNAMODB_ENDPOINT_URL`（ローカル開発用）
- リージョン: `ap-northeast-1` （デフォルト）
- Decimal型で数値精度を保証

## エラーハンドリング

### HTTPException
- 401 Unauthorized - トークン無効・期限切れ
- 404 Not Found - リソース不存在
- 400 Bad Request - Google トークン交換失敗

### JWT検証
- HS256 署名（settings.jwt_secret_key）
- 有効期限: 24時間（デフォルト）
- クレーム: `sub` (user_id), `email`, `name`, `jti`, `iat`, `exp`

### 認証フロー
1. フロントエンド → Google OAuth2 Code + CodeVerifier 取得
2. `/auth/google/callback` → Google ID Token 検証
3. DynamoDB にユーザー保存（upsert）
4. JWT セッショントークン生成・返却
5. 以降のリクエスト: Bearer トークン で認証

## テスト概要

### テスト構成（pytest、1800行）
```
test_repositories_*.py  (4ファイル)  - Repository層の CRUD/Query テスト
test_routers_*.py       (4ファイル)  - エンドポイント・認証・ステータスコードテスト
test_schemas_*.py       (4ファイル)  - Pydantic バリデーション・from_dynamo()テスト
conftest.py            - 共通フィクスチャ（AsyncMockDynamoDB、テストクライアント）
```

### モック戦略
- AsyncMock で DynamoDB操作をモック
- `@pytest.fixture` で テストユーザー・サンプルアイテム提供
- `pytest_asyncio` で async/await テスト対応

### テストクライアント
- httpx.AsyncClient + ASGITransport で FastAPI アプリをテスト
- `Depends(get_current_user)` を TestUser で オーバーライド

## 認証・セキュリティ

### CORS
- 許可オリジン: `settings.allowed_origins`（デフォルト: `http://localhost:5173`）
- credentials, methods, headers：全許可

### HTTPBearer
- `Authorization: Bearer <token>` ヘッダで JWT 受信
- 全エンドポイント（`/health`, `/auth/google/callback` 除外）で必須

### Google OAuth2 フロー
- PKCE サポート（code_verifier）
- ID Token 署名検証 + issuer 確認
- google-auth ライブラリで検証

### 環境変数（config.py）
| 変数 | デフォルト | 説明 |
|---|---|---|
| GOOGLE_CLIENT_ID | "" | Google API コンソールから取得 |
| GOOGLE_CLIENT_SECRET | "" | 同上 |
| JWT_SECRET_KEY | "dev-secret-..." | 本番環境で変更必須 |
| DYNAMODB_ENDPOINT_URL | None | ローカル開発: `http://dynamodb:8000` |
