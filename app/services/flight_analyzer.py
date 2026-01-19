from app.clients.llm_client import LLMClient
from app.clients.flight_data_client import FlightDataClient
from app.models.schemas import FlightAnalysisResponse, HiddenFlightOption, RawFlightData
from typing import Optional


class FlightAnalyzerService:
    """フライト分析サービス"""
    
    def __init__(self):
        self.llm_client = LLMClient()
        self.flight_data_client = FlightDataClient()
    
    async def analyze_route(
        self, 
        departure: str, 
        arrival: str, 
        date: Optional[str] = None
    ) -> FlightAnalysisResponse:
        """
        フライトルートを分析
        
        Args:
            departure: 出発地
            arrival: 到着地
            date: 日程（オプション）
            
        Returns:
            FlightAnalysisResponse
        """
        # 1. 実際のフライトデータを取得
        raw_data = await self.flight_data_client.get_flight_offers(
            departure, arrival, date
        )

        # 2. LLM に分析を依頼（実データを渡す）
        result = await self.llm_client.analyze_flight_route(
            departure, arrival, date, raw_data=raw_data
        )
        
        # 3. レスポンスを構築
        route_str = f"{departure} → {arrival}"
        if date:
            route_str += f" ({date})"
        
        hidden_options = [
            HiddenFlightOption(**opt) for opt in result.get("hidden_options", [])
        ]
        
        return FlightAnalysisResponse(
            route=route_str,
            hidden_options=hidden_options,
            avoid_tips=result.get("avoid_tips", ""),
            raw_data=raw_data
        )
