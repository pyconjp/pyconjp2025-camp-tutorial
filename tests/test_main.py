"""
main モジュールのテスト
"""

from fastapi.testclient import TestClient

from main import AUTH_KEY, app
from searchapi import QueryArgs

client = TestClient(app)


def test_index_default():
    """
    index 関数のテスト（デフォルト値）
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "こんにちは、匿名さん"


def test_index_with_name():
    """
    index 関数のテスト（名前指定）
    """
    response = client.get("/?name=テスト")
    assert response.status_code == 200
    assert response.json() == "こんにちは、テストさん"


def test_single_endpoint(monkeypatch):
    """
    single 関数のテスト（正常系）
    """
    # モックの戻り値を設定
    mock_result = "これはテスト回答です。"
    mock_args = QueryArgs(
        query="テスト質問",
        role="あなたは親切なアシスタントです。",
        model_name="gemini-2.0-flash",
        temperature=0.7,
        max_tokens=1024,
    )

    # query_gemini関数をモックする
    def mock_query_gemini(*args, **kwargs):
        return mock_result, mock_args

    monkeypatch.setattr("main.query_gemini", mock_query_gemini)

    # テストリクエスト
    response = client.post(
        "/single",
        json={
            "key": AUTH_KEY,
            "q": "テスト質問",
            "options": {"model": "gemini-2.0-flash", "max_tokens": 1024},
        },
    )

    # 結果の確認
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "meta" in data
    assert "duration" in data["meta"]

    # Pytestでは関数呼び出しを直接検証できないので、
    # 結果が期待どおりであることを確認する（関数が正しく呼び出された間接的な証拠）
    assert data["data"]["result"] == mock_result
    assert data["data"]["args"]["query"] == "テスト質問"
    assert data["data"]["args"]["model_name"] == "gemini-2.0-flash"
    assert data["data"]["args"]["max_tokens"] == 1024


def test_single_endpoint_invalid_auth():
    """
    single 関数のテスト（認証エラー）
    """
    response = client.post(
        "/single",
        json={
            "key": "invalid_key",
            "q": "テスト質問",
        },
    )

    # 認証エラーを確認
    assert response.status_code == 401
    assert response.json()["detail"] == "認証キーが無効です"
    # 認証エラーの場合、query_gemini関数は呼ばれないので、
    # 明示的なチェックは不要（早期リターンでquery_geminiは実行されない）
