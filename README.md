# Flight Optimizer AI

**隠れた格安航空券を見つけ出す AI ツール**

LLM（Grok API）を活用して、ユーザーが入力した旅行ルートに対して隠れた安い航空券オプションを提案し、価格操作回避ガイドを提供します。

## 特徴

- 🤖 **AI 分析**: Grok API を使った高度なフライト分析
- ✈️ **隠れたルート**: Hidden City チケットや経由便などの格安オプションを発見
- 🔐 **価格操作回避**: VPN やプライベートブラウジングのヒントを提供
- 🎨 **プレミアムデザイン**: ダークモード + グラスモーフィズムの洗練された UI
- ⚡ **高速**: HTMX による部分更新で快適な UX

## 技術スタック

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: HTMX, Jinja2, Vanilla CSS
- **Deployment**: Vercel (Serverless Functions)
- **LLM**: Grok API (xAI)

## セットアップ

### 1. リポジトリをクローン

```bash
git clone <repository-url>
cd hidden_route_scanner
```

### 2. 依存関係をインストール

```bash
pip install -r requirements.txt
```

### 3. 環境変数を設定

`.env.example` をコピーして `.env` を作成し、API キーを設定します：

```bash
cp .env.example .env
```

`.env` ファイルを編集：

```
GROK_API_KEY=your_actual_grok_api_key_here
```

### 4. ローカルで実行

```bash
python3 scripts/run.py
```

自動的に空いているポートを探して起動します（デフォルトでは http://localhost:8000 から試行します）。

## Vercel へのデプロイ

1. GitHub にプッシュ
2. Vercel ダッシュボードで新しいプロジェクトを作成
3. リポジトリをインポート
4. 環境変数 `GROK_API_KEY` を設定
5. デプロイ

## 開発

詳細な開発ルールは [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

## ライセンス

[LICENSE](LICENSE) を参照してください。