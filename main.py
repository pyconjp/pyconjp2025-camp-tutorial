from fastapi import FastAPI

app = FastAPI(
    title="PyCon JP 2025 Camp Tutorial API",
    description="PyCon JP 2025 Camp Tutorialの API サーバー",
    version="0.1.0",
)


@app.get("/")
def index(name: str = "匿名"):
    """
    ルートエンドポイント

    引数:
    - name: 名前（省略可能、デフォルト値は「匿名」）

    戻り値:
    - 挨拶メッセージ
    """
    return f"こんにちは、{name}さん"


def main():
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
