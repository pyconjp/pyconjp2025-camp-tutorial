import time

from fastapi import FastAPI, HTTPException

from models import (
    AVAILABLE_MODELS,
    ApiResponse,
    MultiQueryItem,
    MultiQueryResponse,
    MultiRequest,
    QueryResponse,
    SingleRequest,
)
from searchapi import grid_query_gemini, query_gemini

app = FastAPI(
    title="PyCon JP 2025 Camp Tutorial API",
    description="PyCon JP 2025 Camp Tutorialの API サーバー",
    version="0.1.0",
)

# 仮の認証キー（実際の運用では環境変数などから取得すべき）
AUTH_KEY = "pyconjp2025"


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


@app.post("/single", response_model=ApiResponse)
def single(data: SingleRequest):
    """
    単一の問い合わせを行うエンドポイント

    引数:
    - request: SingleRequestモデルのリクエスト
      - key: 認証キー
      - q: 質問文字列
      - options: オプション設定（省略可能）
        - model: モデル名（デフォルト: gemini-2.0-flash）
        - max_tokens: 最大トークン数（デフォルト: 1024）

    戻り値:
    - ApiResponse: API応答の基本形式
      - data: QueryResponse
        - result: 回答文字列
        - args: QueryArgs型の辞書
      - meta:
        - duration: 処理時間（秒）
    """
    # 認証キーの確認
    if data.key != AUTH_KEY:
        raise HTTPException(status_code=401, detail="認証キーが無効です")

    start_time = time.time()

    options = data.options
    if options is None:
        model_name = AVAILABLE_MODELS.GEMINI_2_0_FLASH
        max_tokens = 1024
    else:
        model_name = options.model
        max_tokens = options.max_tokens
    try:
        # Gemini APIに問い合わせ
        result, args = query_gemini(
            q=data.q,
            role="あなたは親切なアシスタントです。",
            model_name=model_name,
            temperature=0.7,
            max_tokens=max_tokens,
        )
    except ValueError as e:
        # Gemini APIの環境変数が設定されていない場合など
        raise HTTPException(status_code=500, detail=str(e))
    else:
        end_time = time.time()
        duration = end_time - start_time

        # 応答を作成
        response = ApiResponse(
            data=QueryResponse(
                result=result,
                args=args,
            ),
            meta={"duration": duration},
        )

        return response


@app.post("/multi", response_model=MultiQueryResponse)
def multi(data: MultiRequest):
    """
    複数の問い合わせを行うエンドポイント

    引数:
    - request: MultiRequestモデルのリクエスト
      - key: 認証キー
      - q: 質問文字列
      - options: オプション設定
        - models: モデル名のリスト（デフォルト: [gemini-2.0-flash]）
        - roles: 役割のリスト（デフォルト: ["あなたは親切なアシスタントです。"]）
        - max_tokens: 最大トークン数（デフォルト: 1024）

    戻り値:
    - MultiQueryResponse: 複数の応答を含むAPI応答
      - data: MultiQueryItemのリスト
        - id: 回答のID（1から始まるインデックス）
        - result: 回答文字列
        - args: QueryArgs型の辞書
      - meta:
        - duration: 処理時間（秒）
    """
    # 認証キーの確認
    if data.key != AUTH_KEY:
        raise HTTPException(status_code=401, detail="認証キーが無効です")

    start_time = time.time()

    model_names = tuple(data.options.models)
    roles = tuple(data.options.roles)
    max_tokens = data.options.max_tokens

    try:
        # grid_query_geminiを呼び出して、複数の組み合わせで問い合わせる
        results = grid_query_gemini(
            q=data.q,
            roles=roles,
            model_names=model_names,
            temperature=0.7,
            max_tokens=max_tokens,
        )
    except ValueError as e:
        # Gemini APIの環境変数が設定されていない場合など
        raise HTTPException(status_code=500, detail=str(e))
    else:
        # 回答をMultiQueryItemに変換
        multi_query_items = []
        for idx, (result, args) in enumerate(results, 1):
            multi_query_items.append(
                MultiQueryItem(
                    id=idx,
                    result=result,
                    args=args,
                )
            )
        end_time = time.time()
        duration = end_time - start_time

        # 応答を作成
        response = MultiQueryResponse(
            data=multi_query_items,
            meta={"duration": duration},
        )
        return response


def main():
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
