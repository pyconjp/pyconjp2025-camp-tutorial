"""
searchapi モジュールのテスト
"""

import os
from unittest import mock

import pytest

from searchapi import (
    agrid_query_deepseek,
    aquery_deepseek,
    grid_query_deepseek,
    query_deepseek,
)


class MockChatDeepSeek:
    """ChatDeepSeek のモック"""

    def __init__(self, model, temperature, max_tokens):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def invoke(self, messages):
        """同期版の呼び出しをモック"""
        return mock.MagicMock(content="モックされた応答")


class AsyncMockChatDeepSeek(MockChatDeepSeek):
    """ChatDeepSeek の非同期版モック"""

    async def ainvoke(self, messages):
        """非同期版の呼び出しをモック"""
        return mock.MagicMock(content="非同期でモックされた応答")


@pytest.fixture
def mock_env():
    """環境変数 DEEPSEEK_API_KEY をモックする"""
    with mock.patch.dict(os.environ, {"DEEPSEEK_API_KEY": "mock_api_key"}):
        yield


@pytest.fixture
def mock_chat_deepseek():
    """ChatDeepSeek クラスをモック"""
    with mock.patch("searchapi.ChatDeepSeek", MockChatDeepSeek):
        yield


@pytest.fixture
def mock_async_chat_deepseek():
    """非同期版 ChatDeepSeek クラスをモック"""
    with mock.patch("searchapi.ChatDeepSeek", AsyncMockChatDeepSeek):
        yield


def test_query_deepseek(mock_env, mock_chat_deepseek):
    """query_deepseek 関数のテスト"""
    result, args = query_deepseek(
        q="テストクエリ",
        role="テストロール",
        model_name="deepseek-llm",
        temperature=0.7,
        max_tokens=100,
    )

    # 期待される結果の検証
    assert result == "モックされた応答"
    assert isinstance(args, dict)
    assert args["query"] == "テストクエリ"
    assert args["role"] == "テストロール"
    assert args["model_name"] == "deepseek-llm"
    assert args["temperature"] == 0.7
    assert args["max_tokens"] == 100


def test_grid_query_deepseek(mock_env, mock_chat_deepseek):
    """grid_query_deepseek 関数のテスト"""
    roles = ("テストロール1", "テストロール2")
    model_names = ("deepseek-llm", "deepseek-chat")
    results = grid_query_deepseek(
        q="テストクエリ",
        roles=roles,
        model_names=model_names,
        temperature=0.7,
        max_tokens=100,
    )

    # 期待される結果の検証
    assert len(results) == len(roles) * len(model_names)
    # 各結果を検証
    for result, args in results:
        assert result == "モックされた応答"
        assert isinstance(args, dict)
        assert args["query"] == "テストクエリ"
        assert args["role"] in roles
        assert args["model_name"] in model_names
        assert args["temperature"] == 0.7
        assert args["max_tokens"] == 100


@pytest.mark.asyncio
async def test_aquery_deepseek(mock_env, mock_chat_deepseek):
    """aquery_deepseek 関数のテスト"""
    result, args = await aquery_deepseek(
        q="テストクエリ",
        role="テストロール",
        model_name="deepseek-llm",
        temperature=0.7,
        max_tokens=100,
    )

    # 期待される結果の検証
    assert result == "モックされた応答"
    assert isinstance(args, dict)
    assert args["query"] == "テストクエリ"
    assert args["role"] == "テストロール"
    assert args["model_name"] == "deepseek-llm"
    assert args["temperature"] == 0.7
    assert args["max_tokens"] == 100


@pytest.mark.asyncio
async def test_agrid_query_deepseek(mock_env, mock_chat_deepseek):
    """agrid_query_deepseek 関数のテスト"""
    roles = ("テストロール1", "テストロール2")
    model_names = ("deepseek-llm", "deepseek-chat")
    results = await agrid_query_deepseek(
        q="テストクエリ",
        roles=roles,
        model_names=model_names,
        temperature=0.7,
        max_tokens=100,
    )

    # 期待される結果の検証
    assert len(results) == len(roles) * len(model_names)
    # 各結果を検証
    for result, args in results:
        assert result == "モックされた応答"
        assert isinstance(args, dict)
        assert args["query"] == "テストクエリ"
        assert args["role"] in roles
        assert args["model_name"] in model_names
        assert args["temperature"] == 0.7
        assert args["max_tokens"] == 100


def test_no_api_key():
    """API キーが設定されていない場合のエラーテスト"""
    with mock.patch.dict(os.environ, {}, clear=True):
        # importを再度行うことでHAS_API_KEYを再評価
        import searchapi

        searchapi.HAS_API_KEY = False
        error_msg = "DEEPSEEK_API_KEY 環境変数が設定されていません。"
        with pytest.raises(ValueError, match=error_msg):
            searchapi.query_deepseek(
                q="テスト",
                role="テストロール",
                model_name="deepseek-llm",
                temperature=0.7,
            )
