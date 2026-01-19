"""
フライト分析サービス
ビジネスロジックを処理するサービス層
"""
from app.clients.llm_client import LLMClient
from app.models.schemas import FlightAnalysisResponse, HiddenFlightOption
from typing import Optional


class FlightAnalyzerService:
    """フライト分析サービス"""
    
    def __init__(self):
        self.llm_client = LLMClient()
    
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
        # LLM に分析を依頼
        result = await self.llm_client.analyze_flight_route(
            departure, arrival, date
        )
        
        # レスポンスを構築
        route_str = f"{departure} → {arrival}"
        if date:
            route_str += f" ({date})"
        
        hidden_options = [
            HiddenFlightOption(**opt) for opt in result.get("hidden_options", [])
        ]
        
        return FlightAnalysisResponse(
            route=route_str,
            hidden_options=hidden_options,
            avoid_tips=result.get("avoid_tips", "")
        )
