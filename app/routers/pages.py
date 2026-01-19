"""
ページルーター
HTMX を使った Web インターフェースのルート定義
"""
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.flight_analyzer import FlightAnalyzerService
from typing import Optional
import json
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
flight_service = FlightAnalyzerService()

# 空港データの読み込み
AIRPORTS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "airports.json")
with open(AIRPORTS_FILE, "r", encoding="utf-8") as f:
    airports_data = json.load(f)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """ホームページ"""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request}
    )


@router.post("/analyze", response_class=HTMLResponse)
async def analyze_flight(
    request: Request,
    departure: str = Form(...),
    arrival: str = Form(...),
    date: Optional[str] = Form(None)
):
    """フライト分析（HTMX パーシャル）"""
    try:
        # 入力の正規化（IATAコードは常に大文字）
        departure_code = departure.strip().upper()
        arrival_code = arrival.strip().upper()

        # 有効な空港コードかチェック
        valid_codes = {a["code"] for a in airports_data}
        if departure_code not in valid_codes or arrival_code not in valid_codes:
            invalid_code = departure_code if departure_code not in valid_codes else arrival_code
            return templates.TemplateResponse(
                "partials/result_partial.html",
                {
                    "request": request,
                    "error": f"無効な空港コードです: {invalid_code}。候補から選択してください。"
                }
            )

        # サービス層で分析を実行
        result = await flight_service.analyze_route(departure_code, arrival_code, date)
        
        # モックモードの場合の通知（任意）
        warning = None
        if flight_service.llm_client.use_mock:
            warning = "現在、APIキーが未設定のためデモ用のデータ（モック）を表示しています。本物の解析を行うには .env に GROK_API_KEY を設定してください。"

        return templates.TemplateResponse(
            "partials/result_partial.html",
            {
                "request": request,
                "result": result,
                "warning": warning
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "partials/result_partial.html",
            {
                "request": request,
                "error": f"分析中にエラーが発生しました: {str(e)}"
            }
        )


@router.get("/search-airports", response_class=HTMLResponse)
async def search_airports(request: Request, q: str = ""):
    """空港検索（HTMX 補完用）"""
    # HTMX から送られるパラメータ名が 'q' でない場合への対応
    if not q:
        params = request.query_params
        if params:
            # 最初のクエリパラメータの値を検索語として使用
            q = next(iter(params.values()), "")
            
    q = q.strip().lower()
    if not q:
        return HTMLResponse(content="")
    
    # 検索ロジック
    matches = []
    
    # 完全一致
    exact_match = [a for a in airports_data if a["code"].lower() == q]
    # 前方一致 (IATAコード)
    starts_with = [a for a in airports_data if a["code"].lower().startswith(q) and a not in exact_match]
    # その他 (名称、都市名)
    others = [
        a for a in airports_data 
        if (q in a["name"].lower() or q in a["city"].lower()) 
        and a not in exact_match and a not in starts_with
    ]
    
    matches = exact_match + starts_with + others
    
    # マッチした候補を <option> タグのリストとして返す
    options = "".join([
        f'<option value="{a["code"]}">{a["city"]} - {a["name"]} ({a["code"]})</option>' 
        for a in matches[:10]  # 最大10件
    ])
    
    return HTMLResponse(content=options)
