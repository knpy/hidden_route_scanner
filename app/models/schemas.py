"""
Pydantic モデル定義
フライト分析のリクエストとレスポンスに使用するデータモデル
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class FlightSearchRequest(BaseModel):
    """フライト検索リクエスト"""
    departure: str = Field(..., description="出発地")
    arrival: str = Field(..., description="到着地")
    date: Optional[str] = Field(None, description="日程（YYYY-MM-DD）")


class HiddenFlightOption(BaseModel):
    """隠れた航空券オプション"""
    route: str = Field(..., description="ルート説明")
    price: str = Field(..., description="価格")
    save: str = Field(..., description="節約率")
    tips: Optional[str] = Field(None, description="追加のヒント")


class FlightAnalysisResponse(BaseModel):
    """フライト分析のレスポンス"""
    route: str = Field(..., description="検索したルート")
    hidden_options: List[HiddenFlightOption] = Field(
        default_factory=list, 
        description="隠れた格安オプション"
    )
    avoid_tips: str = Field(..., description="価格操作回避のヒント")
