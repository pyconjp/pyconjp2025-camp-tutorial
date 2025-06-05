import enum
from typing import Any, TypedDict

from pydantic import BaseModel, Field


class AVAILABLE_MODELS(str, enum.Enum):
    """利用可能なモデルの列挙型"""

    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"


class QueryArgs(TypedDict):
    """DeepSeek APIの戻り値を表す型"""

    query: str
    role: str
    model_name: AVAILABLE_MODELS
    temperature: float
    max_tokens: int | None


class Options(BaseModel):
    """LLMへのオプション設定"""

    model: AVAILABLE_MODELS = Field(
        AVAILABLE_MODELS.GEMINI_2_0_FLASH,
        title="モデル名",
        description="使用するモデルの名前",
    )
    max_tokens: int = Field(
        1024,
        title="最大トークン数",
        description="生成する回答の最大トークン数",
        ge=128,
        le=4096,
    )


class SingleRequest(BaseModel):
    """単一の問い合わせリクエスト"""

    key: str = Field(..., description="認証キー")
    q: str = Field(..., description="質問文字列")
    options: Options | None = Field(
        None, title="オプション設定", description="モデルやトークン数の設定"
    )


class MultiOptions(BaseModel):
    """複数問い合わせのオプション設定"""

    models: tuple[AVAILABLE_MODELS, ...] = Field(
        (AVAILABLE_MODELS.GEMINI_2_0_FLASH,),
        title="モデル名リスト",
        description="使用するモデルの名前のリスト",
    )
    roles: tuple[str, ...] = Field(
        ("あなたは親切なアシスタントです。",),
        title="役割リスト",
        description="AIの役割を指定する文字列のリスト（例：初心者向け、弁護士風など）",
    )
    max_tokens: int = Field(
        1024,
        title="最大トークン数",
        description="生成する回答の最大トークン数",
        ge=128,
        le=4096,
    )


class MultiRequest(BaseModel):
    """複数の問い合わせリクエスト"""

    key: str = Field(..., description="認証キー")
    q: str = Field(..., description="質問文字列")
    options: MultiOptions = Field(
        default_factory=lambda: MultiOptions(
            models=(AVAILABLE_MODELS.GEMINI_2_0_FLASH,),
            roles=("あなたは親切なアシスタントです。",),
            max_tokens=1024,
        ),
        title="オプション設定",
        description="モデル、役割、トークン数の設定",
    )


class QueryResponse(BaseModel):
    """問い合わせの応答"""

    result: str
    args: QueryArgs


class MultiQueryItem(BaseModel):
    """複数問い合わせの応答の各アイテム"""

    id: int
    result: str
    args: QueryArgs


class MultiQueryResponse(BaseModel):
    """複数問い合わせの応答"""

    data: list[MultiQueryItem]
    meta: dict[str, Any]


class ApiResponse(BaseModel):
    """API応答の基本形式"""

    data: QueryResponse
    meta: dict[str, Any]
