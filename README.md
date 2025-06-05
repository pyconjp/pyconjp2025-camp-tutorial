# pyconjp2025-camp-tutorial

PyCon JP 2025 の合宿時に [FastAPI](https://fastapi.tiangolo.com/) のチュートリアルを実施する

- FastAPI で、LLM への問い合わせをまとめて実行できる、API サーバを構築する
- Gemini API を使って、まとめて AI から回答を得られる API サーバを作る
  - 10 件の別観点の質問を、AI に問い合わせ
  - まとめて回答が得られる

# 環境設定

## 初期構築

この内容は、このチュートリアルを作るためのものです。
以下は実施済みなので、後述する `利用者向け構築` の項目を参照してください。

```bash
$ uv init -p python3.13
$ uv add "fastapi[all]"
$ uv add "langchain[langchain-google-genai]"
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

## Google Gemini API の取得方法と設定

- Google AI Studio の サイトへ https://ai.google.dev/aistudio?hl=ja
- サイトに Google アカウントでログインする
- Google AI Studio のログインを行う
- Build with the Gemini API -> 「Get API key」をクリック
- 規約に同意する
- 「API キーを作成」-> 「新しいプロジェクトで API キーを作成」
- Key は画面に表示されるので **漏らさない** ように個人で管理する

Mac/Linux

```
% export GOOGLE_API_KEY=xxxxxxxxxxxxxx
```

Windows

```
> $Env:GOOGLE_API_KEY = "xxxxxxx"
```

# チュートリアルの進め方

[チュートリアル対象者のレベルごとの進め方](tutorial.md) ドキュメントを参照

## おまけ: VS Code セットアップ手順

[Visual Studio Code](https://code.visualstudio.com) (以下 VS Code) を使う人向けのセットアップ手順(`git clone` 後)を記載します。
既に VS Code で Python 環境を設定済み、または他のエディタを使用している人はスキップして問題ありません。

1. 任意: VS Code で[新規プロファイル](https://code.visualstudio.com/docs/configure/profiles)を作成
   1. 他の言語などで VS Code を開発に使用している場合は新規プロファイルを推奨
1. メニューから「フォルダを開く (Open Folder)」を選択し、クローンしたリポジトリを選択
1. 右下に以下のような「おすすめ拡張機能をインストールするか」のポップアップ ダイアログが出るので「インストール」を押下
   1. または左端のアクティビティ バーにある拡張機能のアイコンをクリックし、検索窓に `@recommended` と入力して表示される拡張機能をインストールする
   1. メッセージ(日): このリポジトリ 用のおすすめ拡張機能 Microsoft、tamasfe、その他からの拡張機能 をインストールしますか?
   1. メッセージ(英): Do you want to install the recommended extensions from Microsoft, tamasfe and others for this repository?
1. 任意: 右下に以下メッセージのような「Python インタープリタを選択」とポップアップ ダイアログが出る場合は Python インタープリタを指定する
   1. インタープリターの場所は `.venv/bin/python` (Python 3.13.z)
   1. メッセージ(日): 無効な Python インタープリターが選択されています。IntelliSense、リンティング、デバッグなどの機能を有効にするために変更してみてください。インタープリターが無効である理由の詳細については、出力を参照してください。
   1. メッセージ(英): An Invalid Python interpreter is selected, please try changing it to enable features such as IntelliSense, linting, and debugging. See output for more details regarding why the interpreter is invalid.
1. 自動フォーマットが有効になっているか確認
   1. リポジトリ直下にある `main.py` を開いて 1 行目 (`main` 関数の前) に適当に改行を挿入
   1. 左上メニューから「保存」を実施(または `Ctrl/Cmd + S` ショートカット)
   1. 自動でフォーマットされれば OK

## 実行方法

### 起動

uv を使用する場合：

```
uv run python main.py
```

venv を使用する場合：

```
(venv) python main.py
```

サーバーが起動したら、ブラウザで http://127.0.0.1:8000 にアクセスできます。
また、API ドキュメントは http://127.0.0.1:8000/docs または http://127.0.0.1:8000/redoc で閲覧できます。

### テスト実行

```
% uv run pytest tests/
```

venv の場合

```
(venv) % pytest tests/
```

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
    - `model`: デフォルトで `gemini-2.0-flush`
    - `max_tokens`: デフォルトで 1024
  - 個別 (multi の場合)
    - `models`: `list[model]` 複数のモデルを利用できるようにする
      - "gemini-2.0-flash",
      - "gemini-1.5-flash",
      - "gemini-2.5-flash",
    - `prefixes`: `list[str]` 質問文の前にいれる文言 (例: `["初心者向けに答えて", "弁護士風に答えて"]`)
