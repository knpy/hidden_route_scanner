"""
ページルーター
HTMX を使った Web インターフェースのルート定義
"""
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.flight_analyzer import FlightAnalyzerService
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
flight_service = FlightAnalyzerService()


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
        # サービス層で分析を実行
        result = await flight_service.analyze_route(departure, arrival, date)
        
        return templates.TemplateResponse(
            "partials/result_partial.html",
            {
                "request": request,
                "result": result
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
