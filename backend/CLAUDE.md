# バックエンド コーディング規約

## Python / FastAPI

- PEP 8 準拠
- 型ヒント: すべての関数引数・戻り値に型ヒント必須
- 命名: 変数・関数は `snake_case`、クラスは `PascalCase`
- リクエスト/レスポンス: Pydantic モデルで定義する
- 定数: モジュールレベルに `UPPER_SNAKE_CASE` で定義する

## テスト（pytest）

- テストファイルは `backend/tests/` に配置し、`test_*.py` で命名する

## コマンド

```bash
python export_openapi.py  # Pydantic → openapi.json 書き出し
```
