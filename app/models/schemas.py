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


class FlightOffer(BaseModel):
    """実在するフライトのオファー情報"""
    airline: str = Field(..., description="航空会社")
    flight_number: str = Field(..., description="便名")
    departure_time: str = Field(..., description="出発時刻")
    arrival_time: str = Field(..., description="到着時刻")
    price: float = Field(..., description="価格")
    currency: str = Field(..., description="通貨")
    booking_link: Optional[str] = Field(None, description="予約リンク")


class RawFlightData(BaseModel):
    """外部APIから取得した生のフライトデータ"""
    source: str = Field(..., description="データソース（Amadeus等）")
    offers: List[FlightOffer] = Field(default_factory=list, description="フライトオファーのリスト")


class HiddenFlightOption(BaseModel):
    """隠れた航空券オプション"""
    route: str = Field(..., description="ルート説明")
    price: str = Field(..., description="価格")
    save: str = Field(..., description="節約率")
    tips: Optional[str] = Field(None, description="追加のヒント")
    real_fights: List[FlightOffer] = Field(default_factory=list, description="関連する実際のフライト")


class FlightAnalysisResponse(BaseModel):
    """フライト分析のレスポンス"""
    route: str = Field(..., description="検索したルート")
    hidden_options: List[HiddenFlightOption] = Field(
        default_factory=list, 
        description="隠れた格安オプション"
    )
    avoid_tips: str = Field(..., description="価格操作回避のヒント")
    raw_data: Optional[RawFlightData] = Field(None, description="参考にした実データ")
