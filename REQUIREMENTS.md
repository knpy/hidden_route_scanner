# **Flight Optimizer AI \- 初期仕様書（Vercel \+ FastAPI \+ HTMX版）**

## **1\. プロジェクト概要**

* **目的**: ユーザーが入力した旅行ルートに対して、LLM（Grok APIなど）を使って隠れた安い航空券オプションを提案 \+ 価格操作回避ガイドを提供  
* **スタック**:  
  * **Backend**: FastAPI (Python 3.11+)  
  * **Frontend**: HTMX \+ Jinja2 (最小JS、サーバーサイドレンダリング)  
  * **Deployment**: Vercel (Serverless Functions, Hobbyプラン無料スタート)  
  * **LLM**: Grok API (or OpenAI fallback) – 外部APIキー設定  
* **フェーズ**: Phase 1 – MVP（ローカル → Vercelデプロイ可能）

## **2\. ディレクトリ構造（Vercel最適化版）**

Vercelは api/ フォルダ内のPythonファイルをServerless Functionとして扱うので、この構造がベストです。

flight-optimizer/  
├── api/  
│   └── index.py          \# ← メインのFastAPIアプリ（Vercelがここを見る）  
├── templates/            \# Jinja2 HTMLテンプレート（HTMX用）  
│   ├── base.html  
│   ├── index.html  
│   ├── result.html  
│   └── partials/  
│       └── form.html     \# HTMXで部分更新用  
├── static/               \# CSS/JS（HTMXはCDNでOK）  
│   └── style.css  
├── requirements.txt  
├── vercel.json           \# ← Vercel設定必須  
└── .gitignore

## **3\. vercel.json（必須！これでゼロコンフィグに近い）**

* **maxDuration**: 30秒（LLMコールが遅い場合に調整。デフォルト15秒）  
* 将来拡張時は api/ 以下に複数ファイル置いてもOK（Vercelが自動認識）

{  
  "version": 2,  
  "builds": \[  
    {  
      "src": "api/index.py",  
      "use": "@vercel/python"  
    }  
  \],  
  "routes": \[  
    {  
      "src": "/(.\*)",  
      "dest": "api/index.py"  
    }  
  \],  
  "functions": {  
    "api/index.py": {  
      "memory": 1024,  
      "maxDuration": 30  
    }  
  }  
}

## **4\. requirements.txt（最小限スタート）**

fastapi==0.115.0  
uvicorn==0.32.0  
jinja2==3.1.4  
httpx==0.27.2          \# LLM/APIコール用  
python-dotenv==1.0.1   \# .env管理

## **5\. api/index.py（メインエントリーポイント – ローカル/Vercel両対応）**

from fastapi import FastAPI, Request, Form  
from fastapi.responses import HTMLResponse  
from fastapi.templating import Jinja2Templates  
from fastapi.staticfiles import StaticFiles  
import os  
from dotenv import load\_dotenv

load\_dotenv()  \# Vercelでは環境変数設定でOK

app \= FastAPI()

templates \= Jinja2Templates(directory="templates")  
app.mount("/static", StaticFiles(directory="static"), name="static")

\# ダミーLLMコール（後でGrok/OpenAIに置き換え）  
def mock\_llm\_analysis(route: str):  
    return {  
        "hidden\_options": \[  
            {"route": "Tokyo → Narita → Osaka (hidden city)", "price": "¥18,000", "save": "40%"},  
            {"route": "Direct Tokyo → Osaka", "price": "¥30,000", "save": "0%"}  
        \],  
        "avoid\_tips": "インコグニート \+ VPNで検索しよう！"  
    }

@app.get("/", response\_class=HTMLResponse)  
async def home(request: Request):  
    return templates.TemplateResponse(  
        "index.html", {"request": request, "result": None}  
    )

@app.post("/analyze", response\_class=HTMLResponse)  
async def analyze(  
    request: Request,  
    departure: str \= Form(...),  
    arrival: str \= Form(...),  
    date: str \= Form(None)  
):  
    route \= f"{departure} → {arrival} ({date or '任意日'})"  
    result \= mock\_llm\_analysis(route)  \# ← ここを本物のLLMに  
    return templates.TemplateResponse(  
        "partials/result.html",  
        {"request": request, "result": result, "route": route}  
    )

\# ローカル実行用（Vercelでは不要）  
if \_\_name\_\_ \== "\_\_main\_\_":  
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000)

## **6\. templates/index.html（HTMXで部分更新）**

\<\!DOCTYPE html\>  
\<html lang="ja"\>  
\<head\>  
    \<meta charset="UTF-8"\>  
    \<title\>Flight Optimizer AI\</title\>  
    \<script src="\[https://unpkg.com/htmx.org@2.0.0\](https://unpkg.com/htmx.org@2.0.0)"\>\</script\>  
    \<link rel="stylesheet" href="/static/style.css"\>  
\</head\>  
\<body\>  
    \<h1\>Flight Optimizer AI\</h1\>  
      
    \<form hx-post="/analyze" hx-target="\#result" hx-swap="innerHTML"\>  
        \<label\>出発地: \<input type="text" name="departure" required\>\</label\>\<br\>  
        \<label\>目的地: \<input type="text" name="arrival" required\>\</label\>\<br\>  
        \<label\>日程: \<input type="date" name="date"\>\</label\>\<br\>  
        \<button type="submit"\>分析する\</button\>  
    \</form\>

    \<div id="result"\>  
        \<\!-- 結果がここにHTMXで差し込まれる \--\>  
    \</div\>  
\</body\>  
\</html\>

## **7\. templates/partials/result.html（HTMX部分更新用）**

{% if result %}  
    \<h2\>{{ route }} の分析結果\</h2\>  
      
    \<h3\>隠れた安いオプション\</h3\>  
    \<ul\>  
        {% for opt in result.hidden\_options %}  
            \<li\>{{ opt.route }} → {{ opt.price }} ({{ opt.save }}節約)\</li\>  
        {% endfor %}  
    \</ul\>  
      
    \<h3\>価格操作回避Tips\</h3\>  
    \<p\>{{ result.avoid\_tips }}\</p\>  
{% else %}  
    \<p\>分析中...\</p\>  
{% endif %}

## **8\. 次のステップ（ローカル → Vercel）**

1. 上記ファイルをコピーしてプロジェクト作成  
2. pip install \-r requirements.txt  
3. uvicorn api.index:app \--reload でローカル起動（http://localhost:8000）  
4. GitHubにpush  
5. Vercelダッシュボード → New Project → GitHubリポジトリインポート → Deploy（無料！）  
6. デプロイ後URLで確認（自動でhttpsになる）

**今後の拡張:**

* 問題なければ、次は本物のLLM統合（Grok APIキー環境変数）  
* エラーハンドリング  
* リアルフライトAPI連携（Google Flightsなど）を追加していきましょう。

**TODO / 要望:**

* 何か修正したい部分や「次にこれを実装して！」があれば教えてください！  
  * （例: フォームに空港コード自動補完、結果にテーブル表示など）