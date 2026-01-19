# Flight Optimizer AI - プロジェクト設定

このファイルは、Antigravity がこのプロジェクトで従うべきガイドラインとコンテキストを定義します。

## プロジェクト概要
ユーザーが入力した旅行ルートに対して、LLM（Grok APIなど）を使って隠れた安い航空券オプションを提案し、価格操作回避ガイドを提供します。

## 技術スタック
- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: HTMX, Jinja2, Vanilla CSS
- **Deployment**: Vercel (Serverless Functions)
- **LLM**: Grok API (xAI)

## コーディング規約
- **言語**: 回答およびドキュメントは日本語で行う。コード内のコメントも日本語を推奨。
- **アーキテクチャ**: `api/` (Vercel用) と `app/` (本体ロジック) を分離したモジュール構造を維持する。
- **デザイン**: プレミアムでモダンな外観（ダークモード、グラスモーフィズム）を優先する。
- **依存関係**: `requirements.txt` を最新に保つ。

## 開発フロー
1. `task.md` で進捗を管理。
2. 大きな変更の前には `implementation_plan.md` を作成し、ユーザーの承認を得る。
3. 実装後は `walkthrough.md` で変更内容を報告する。
