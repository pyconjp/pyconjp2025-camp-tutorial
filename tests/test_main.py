"""
main モジュールのテスト
"""

from fastapi.testclient import TestClient

from main import app


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
