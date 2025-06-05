"""
Gemini APIに対して問い合わせを行うモジュール

このモジュールには3つの機能を持つ:
- 一つの問い合わせだけを行う `query_gemini` 関数
- 複数の問い合わせを実行する `grid_query_gemini` 関数
- 複数の問い合わせを非同期に実行する `agrid_query_gemini` 関数
"""

import asyncio
import logging
import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from models import AVAILABLE_MODELS, QueryArgs

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if os.getenv("GOOGLE_API_KEY") is None:
    HAS_API_KEY = False
    logger.warning(
        "GOOGLE_API_KEY 環境変数が設定されていません。"
        "Gemini APIを使用するには、環境変数 GOOGLE_API_KEY を設定してください。"
    )
else:
    HAS_API_KEY = True


def query_gemini(
    q: str,
    role: str,
    model_name: AVAILABLE_MODELS,
    temperature: float,
    max_tokens: int | None = None,
) -> tuple[str, QueryArgs]:
    """Gemini APIに単一の問い合わせを行う関数

    Args:
        q: クエリ文字列
        role: 役割(System引数)
        model_name: モデル名
        temperature: ランダムさ
        max_tokens: トークン数（省略可能）

    Returns:
        tuple[str, Dict[str, Union[str, int, float, None]]]:
          - APIからの戻り文字列
          - 引数の値をオブジェクトで返す
    """
    if not HAS_API_KEY:
        raise ValueError("GOOGLE_API_KEY 環境変数が設定されていません。")
    chat = ChatGoogleGenerativeAI(
        model=model_name, temperature=temperature, max_tokens=max_tokens
    )

    messages = [SystemMessage(content=role), HumanMessage(content=q)]

    result = chat.invoke(messages)

    args_dict: QueryArgs = {
        "query": q,
        "role": role,
        "model_name": model_name,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    # result.contentをstr型に確実に変換
    content_str = str(result.content)
    return content_str, args_dict


def grid_query_gemini(
    q: str,
    roles: tuple[str, ...],
    model_names: tuple[AVAILABLE_MODELS, ...],
    temperature: float,
    max_tokens: int | None = None,
) -> list[tuple[str, QueryArgs]]:
    """Gemini APIに複数の問い合わせを行う関数

    役割とモデル複数のパターンをすべて問い合わせる

    Args:
        q: クエリ文字列
        roles: 役割(System引数)のタプル
        model_names: モデル名のタプル
        temperature: ランダムさ
        max_tokens: トークン数（省略可能）

    Returns:
        List[Tuple[str, Dict[str, Union[str, int, float, None]]]]:
          query_gemini関数の戻り値のリスト
    """
    if not HAS_API_KEY:
        raise ValueError("GOOGLE_API_KEY 環境変数が設定されていません。")
    results = []

    for model_name in model_names:
        for role in roles:
            result, args = query_gemini(
                q=q,
                role=role,
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            results.append((result, args))

    return results


async def aquery_gemini(
    q: str,
    role: str,
    model_name: AVAILABLE_MODELS,
    temperature: float,
    max_tokens: int | None = None,
) -> tuple[str, QueryArgs]:
    """Gemini APIに単一の問い合わせを非同期で行う関数

    query_gemini関数の非同期版関数

    Args:
        q: クエリ文字列
        role: 役割(System引数)
        model_name: モデル名
        temperature: ランダムさ
        max_tokens: トークン数（省略可能）

    Returns:
        tuple[str, Dict[str, Union[str, int, float, None]]]:
          query_gemini関数の戻り値
    """
    if not HAS_API_KEY:
        raise ValueError("GOOGLE_API_KEY 環境変数が設定されていません。")

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        query_gemini,
        q,
        role,
        model_name,
        temperature,
        max_tokens,
    )


async def agrid_query_gemini(
    q: str,
    roles: tuple[str, ...],
    model_names: tuple[AVAILABLE_MODELS, ...],
    temperature: float,
    max_tokens: int | None = None,
) -> list[tuple[str, QueryArgs]]:
    """Gemini APIに複数の問い合わせを非同期で実行する関数

    grid_query_gemini関数の非同期版関数

    Args:
        q: クエリ文字列
        roles: 役割(System引数)のタプル
        model_names: モデル名のタプル
        temperature: ランダムさ
        max_tokens: トークン数（省略可能）

    Returns:
        List[Tuple[str, Dict[str, Union[str, int, float, None]]]]:
          query_gemini関数の戻り値のリスト
    """
    if not HAS_API_KEY:
        raise ValueError("GOOGLE_API_KEY 環境変数が設定されていません。")
    tasks = []

    for model_name in model_names:
        for role in roles:
            task = aquery_gemini(
                q=q,
                role=role,
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            tasks.append(task)

    # 並列に実行して結果を待つ
    results = await asyncio.gather(*tasks)

    return results
