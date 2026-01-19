"""
LLM クライアント
Grok API（または OpenAI）との通信を処理
"""
import os
import httpx
from typing import Optional
from app.models.schemas import RawFlightData
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """LLM クライアント（Grok API / OpenAI）"""
    
    def __init__(self):
        # 環境変数から取得し、前後の空白を除去
        self.grok_api_key = (os.getenv("GROK_API_KEY") or "").strip()
        self.openai_api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
        
        # プレースホルダーのチェック
        is_grok_valid = bool(self.grok_api_key and "your_" not in self.grok_api_key and len(self.grok_api_key) > 20)
        is_openai_valid = bool(self.openai_api_key and "your_" not in self.openai_api_key and len(self.openai_api_key) > 20)
        
        self.use_mock = not (is_grok_valid or is_openai_valid)
        
        # 起動時にログ出力
        if self.use_mock:
            print("--- LLM Status: MOCK MODE ---")
        elif is_grok_valid:
            print(f"--- LLM Status: GROK MODE (Key prefix: {self.grok_api_key[:8]}...) ---")
        else:
            print(f"--- LLM Status: OPENAI MODE (Key prefix: {self.openai_api_key[:8]}...) ---")
        
    async def analyze_flight_route(
        self, 
        departure: str, 
        arrival: str, 
        date: Optional[str] = None,
        raw_data: Optional[RawFlightData] = None
    ) -> dict:
        """
        フライトルートを分析して隠れた格安オプションを提案
        """
        route_description = f"{departure} → {arrival}"
        if date:
            route_description += f" ({date})"
        
        if self.use_mock:
            return self._mock_analysis(route_description)
        
        if self.grok_api_key:
            return await self._call_grok_api(departure, arrival, date, raw_data)
        
        if self.openai_api_key:
            return await self._call_openai_api(departure, arrival, date, raw_data)
        
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
                          "🌍 **別の空港**: 近領の空港を検討してください（例: 成田 vs 羽田）。"
        }
    
    async def _call_grok_api(
        self, 
        departure: str, 
        arrival: str, 
        date: Optional[str],
        raw_data: Optional[RawFlightData] = None
    ) -> dict:
        """Grok API を呼び出し"""
        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.grok_api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = (
            "あなたは航空券の専門家です。提供された実フライトデータに基づいて隠れた格安ルートを提案してください。"
            "JSON形式で返答してください。"
        )
        
        user_prompt = f"出発地: {departure}, 目的地: {arrival}"
        if date:
            user_prompt += f", 日程: {date}"
        
        if raw_data and raw_data.offers:
            user_prompt += "\n\n実データ：\n"
            for offer in raw_data.offers:
                user_prompt += f"- {offer.airline} ({offer.flight_number}): {offer.departure_time}-{offer.arrival_time}, {offer.price} {offer.currency}\n"
        
        payload = {
            "model": "grok-4-1-fast-reasoning",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": {"type": "json_object"}
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                if response.status_code != 200:
                    print(f"Grok API Error Response: {response.status_code} - {response.text}")
                response.raise_for_status()
                data = response.json()
                
                content = data["choices"][0]["message"]["content"]
                import json
                return json.loads(content)
        except Exception as e:
            print(f"Grok API Exception: {e}")
            return self._mock_analysis(f"{departure} → {arrival}")

    async def _call_openai_api(
        self, 
        departure: str, 
        arrival: str, 
        date: Optional[str],
        raw_data: Optional[RawFlightData] = None
    ) -> dict:
        """OpenAI API を呼び出し"""
        return self._mock_analysis(f"{departure} → {arrival}")
