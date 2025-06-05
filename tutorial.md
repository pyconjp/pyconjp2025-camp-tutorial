# チュートリアル対象者のレベルごとの進め方

以下の段階ごとに、リンクにあるソースコードをダウンロードして(または git tag で切り替えて)チュートリアルを行う

- (1) [オススメ] エンドポイントを増やし、バリデーションを実装
- (2) [初心者向け] 動かしてみてから、改造する
- (3) [中級者向け] FastAPI のエンドポイントを 0 から作る
- (4) [上級者向け] 非同期対応の実装を行う
- (5) [自由にやりたい] 環境設定のみの状況から自由に FastAPI で API サーバを作る

チュートリアルは FastAPI の公式を利用する。日本語版を参考にするが一部古い記述があるので英語版も確認する必要がある

- [FastAPI 日本語版チュートリアル](https://fastapi.tiangolo.com/ja/tutorial/)
- [FastAPI 英語版チュートリアル](https://fastapi.tiangolo.com/tutorial/)

## (1) エンドポイントを増やし、バリデーションを実装

一つのエンドポイントから徐々に増やしていき、バリデーションなどを学ぶ

https://github.com/pyconjp/pyconjp2025-camp-tutorial/releases/tag/single-no-validation-2

## (2) 動かしてみてから、改造する

非同期を除くエンドポイントが完成しているところから、動かしてみて改造する

https://github.com/pyconjp/pyconjp2025-camp-tutorial/releases/tag/multi-validation-2

## (3) FastAPI のエンドポイントを 0 から作る

手を動かしながら一緒に API サーバを作る（LangChain 部分はモジュールを呼び出すだけ）

https://github.com/pyconjp/pyconjp2025-camp-tutorial/releases/tag/langchain-2

## (4) 非同期対応の実装を行う

非同期部分の API の作り込みを行う

https://github.com/pyconjp/pyconjp2025-camp-tutorial/releases/tag/multi-validation-2

## (5) 環境設定のみの状況から自由に FastAPI で API サーバを作る

別用途で API サーバを作ってみたい人向け

https://github.com/pyconjp/pyconjp2025-camp-tutorial/releases/tag/init-2

# 20250605 時点の完成版

https://github.com/pyconjp/pyconjp2025-camp-tutorial/releases/tag/multi-async-2
