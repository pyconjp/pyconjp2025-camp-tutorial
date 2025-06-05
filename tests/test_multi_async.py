"""
multi-async エンドポイントのテスト
"""

import pytest
from httpx import AsyncClient

from main import AUTH_KEY, app


@pytest.mark.asyncio
async def test_multi_async_endpoint(monkeypatch):
    """
    multi_async 関数のテスト（正常系）
    """
    # モックの戻り値を設定
    mock_results = [
        (
            "これは非同期モデル1の回答です。",
            {
                "query": "テスト質問",
                "role": "初心者向けに答えて",
                "model_name": "gemini-2.0-flash",
                "temperature": 0.7,
                "max_tokens": 1024,
            },
        ),
        (
            "これは非同期モデル2の回答です。",
            {
                "query": "テスト質問",
                "role": "弁護士風に答えて",
                "model_name": "gemini-2.5-flash",
                "temperature": 0.7,
                "max_tokens": 1024,
            },
        ),
    ]

    # agrid_query_gemini関数をモックする
    async def mock_agrid_query_gemini(*args, **kwargs):
        return mock_results

    monkeypatch.setattr("main.agrid_query_gemini", mock_agrid_query_gemini)

    # テストリクエスト
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/multi-async",
            json={
                "key": AUTH_KEY,
                "q": "テスト質問",
                "options": {
                    "models": ["gemini-2.0-flash", "gemini-2.5-flash"],
                    "roles": ["初心者向けに答えて", "弁護士風に答えて"],
                    "max_tokens": 1024,
                },
            },
        )

        # 結果の確認
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "meta" in data
        assert "duration" in data["meta"]

        # 返却データの検証
        assert len(data["data"]) == 2
        assert data["data"][0]["id"] == 1
        assert data["data"][0]["result"] == "これは非同期モデル1の回答です。"
        assert data["data"][1]["id"] == 2
        assert data["data"][1]["result"] == "これは非同期モデル2の回答です。"


@pytest.mark.asyncio
async def test_multi_async_endpoint_invalid_auth():
    """
    multi_async 関数のテスト（認証エラー）
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/multi-async",
            json={
                "key": "invalid_key",
                "q": "テスト質問",
                "options": {
                    "models": ["gemini-2.0-flash"],
                    "roles": ["初心者向けに答えて"],
                    "max_tokens": 1024,
                },
            },
        )

        # 認証エラーを確認
        assert response.status_code == 401
        assert response.json()["detail"] == "認証キーが無効です"
