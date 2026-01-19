"""
FastAPI メインアプリケーション
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import pages

app = FastAPI(
    title="Flight Optimizer AI",
    description="隠れた格安航空券を見つけるAIツール",
    version="0.1.0"
)

# 静的ファイルをマウント
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ルーターを追加
app.include_router(pages.router)


@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {"status": "ok"}
