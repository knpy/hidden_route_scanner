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
        
        # プレースホルダーのチェック
        is_grok_valid = self.grok_api_key and "your_grok" not in self.grok_api_key
        is_openai_valid = self.openai_api_key and "your_openai" not in self.openai_api_key
        
        self.use_mock = not (is_grok_valid or is_openai_valid)
        
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
        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.grok_api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = (
            "あなたは航空券の専門家です。ユーザーのルートに対して、隠れた格安オプションを提案してください。"
            "特に以下の手法を検討してください：\n"
            "1. Hidden City チケット (最終目的地を越えた航空券を予約し、経由地で降りる)\n"
            "2. 複数航空券の組み合わせ (Self-transfer)\n"
            "3. 近くの代替空港の利用\n"
            "4. 曜日や時間帯の最適化\n\n"
            "レスポンスは必ず以下のJSON形式で返してください：\n"
            "{\n"
            "  \"hidden_options\": [\n"
            "    {\"route\": \"説明\", \"price\": \"価格\", \"save\": \"節約率%\", \"tips\": \"アドバイス\"}\n"
            "  ],\n"
            "  \"avoid_tips\": \"価格操作を避けるための詳細なアドバイス（マークダウン形式）\"\n"
            "}"
        )
        
        user_prompt = f"出発地: {departure}, 目的地: {arrival}"
        if date:
            user_prompt += f", 日程: {date}"
        
        payload = {
            "model": "grok-beta",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": {"type": "json_object"}
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                
                # チャット完了のコンテンツをパース
                content = data["choices"][0]["message"]["content"]
                import json
                return json.loads(content)
        except Exception as e:
            print(f"Grok API Error: {e}")
            return self._mock_analysis(f"{departure} → {arrival}")

    async def _call_openai_api(
        self, 
        departure: str, 
        arrival: str, 
        date: Optional[str]
    ) -> dict:
        """OpenAI API を呼び出し"""
        # フォールバック用。必要に応じて実装
        return self._mock_analysis(f"{departure} → {arrival}")
