import json

from app.main import app

if __name__ == "__main__":
    schema = app.openapi()
    with open("openapi.json", "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)
    print("openapi.json generated.")
