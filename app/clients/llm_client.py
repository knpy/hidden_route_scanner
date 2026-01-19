"""
LLM クライアント
Grok API（または OpenAI）との通信を処理
"""
import os
import httpx
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """LLM クライアント（Grok API / OpenAI）"""
    
    def __init__(self):
        self.grok_api_key = os.getenv("GROK_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.use_mock = not (self.grok_api_key or self.openai_api_key)
        
    async def analyze_flight_route(
        self, 
        departure: str, 
        arrival: str, 
        date: Optional[str] = None
    ) -> dict:
        """
        フライトルートを分析して隠れた格安オプションを提案
        
        Args:
            departure: 出発地
            arrival: 到着地
            date: 日程（オプション）
            
        Returns:
            分析結果の辞書
        """
        route_description = f"{departure} → {arrival}"
        if date:
            route_description += f" ({date})"
        
        # モックモード（API キーがない場合）
        if self.use_mock:
            return self._mock_analysis(route_description)
        
        # Grok API を優先的に使用
        if self.grok_api_key:
            return await self._call_grok_api(departure, arrival, date)
        
        # OpenAI をフォールバックとして使用
        if self.openai_api_key:
            return await self._call_openai_api(departure, arrival, date)
        
        return self._mock_analysis(route_description)
    
    def _mock_analysis(self, route: str) -> dict:
        """モック分析（デモ用）"""
        return {
            "hidden_options": [
                {
                    "route": f"{route} (経由地: ソウル)",
                    "price": "¥25,000",
                    "save": "35%",
                    "tips": "仁川空港経由で乗り継ぎ1回"
                },
                {
                    "route": f"{route} (Hidden City チケット)",
                    "price": "¥28,000",
                    "save": "28%",
                    "tips": "最終目的地を超えた便を予約し、途中下車"
                },
                {
                    "route": f"{route} (直行便)",
                    "price": "¥39,000",
                    "save": "0%",
                    "tips": "標準的な直行便"
                },
            ],
            "avoid_tips": "🔐 **プライバシー保護**: VPN + プライベートブラウジングで検索すると、クッキーベースの価格操作を回避できます。\n\n"
                          "📅 **柔軟な日程**: 出発日を±3日ずらすだけで大幅に安くなることがあります。\n\n"
                          "🌍 **別の空港**: 近隣の空港を検討してください（例: 成田 vs 羽田）。"
        }
    
    async def _call_grok_api(
        self, 
        departure: str, 
        arrival: str, 
        date: Optional[str]
    ) -> dict:
        """Grok API を呼び出し"""
        # TODO: Grok API の実装
        # 現在はモックを返す
        return self._mock_analysis(f"{departure} → {arrival}")
    
    async def _call_openai_api(
        self, 
        departure: str, 
        arrival: str, 
        date: Optional[str]
    ) -> dict:
        """OpenAI API を呼び出し"""
        # TODO: OpenAI API の実装
        # 現在はモックを返す
        return self._mock_analysis(f"{departure} → {arrival}")
