# pyconjp2025-camp-tutorial

PyCon JP 2025 の合宿時に [FastAPI](https://fastapi.tiangolo.com/) のチュートリアルを実施する

- FastAPI で、LLM への問い合わせをまとめて実行できる、API サーバを構築する
- DeepSeek API を使って、まとめて AI から回答を得られる API サーバを作る
    - 10 件の別観点の質問を、AI に問い合わせ
    - まとめて回答が得られる

# 環境設定

## 初期構築

この内容は、このチュートリアルを作るためのものです。
以下は実施済みなので、後述する `利用者向け構築` の項目を参照してください。

```bash
$ uv init -p python3.13
$ uv add "fastapi[all]"
$ uv add "langchain[deepseek]"
$ uv add --dev ruff pyright pytest pytest-asyncio httpx
```

## 利用者向け構築

uv を使用する場合

```bash
$ uv sync --extra 'dev'
```

venv を利用する場合

```bash
$ python -m venv venv
$ source venv/bin/python
(venv) $ pip install -e ".[dev]"
```

## 実行方法

TBD

- 起動
- テスト実行

## 利用するパッケージ(主なもの)

詳細は `pyproject.toml` を参照してください。

- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://python.langchain.com/docs/introduction/)

# 完成形の状態

- API のエンドポイント(以下の 4 つを作る)
    - `/` 説明文をテキストで表示する GET
    - `/single` 一つの質問を問い合わせ POST
    - `/multi` 複数の問い合わせ POST
    - `/multi-async` 複数の問い合わせを非同期で実行 POST
- API のパラメータ仕様
    - 共通
        - `key`: 仮認証用・・公開した際に誤って大量のリクエストを受け付けないようにするための内部キー(認証としては仮のものと考えたほうがいいが)
        - `q`: 質問文字列
        - `options`:
        - `model`: デフォルトで DeepSeek XXX
        - `max_tokens`: デフォルトで 1024
    - 個別 (multi の場合)
        - `models`: `list[model]` 複数のモデルをりようできるようにする
        - `prefixes`: `list[str]` 質問文の前にいれる文言 (例: `["初心者向けに答えて", "弁護士風に答えて"]`)
