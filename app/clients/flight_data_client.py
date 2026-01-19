"""
外部フライトデータクライアント (SerpApi 版)
Google Flights API を通じて LCC を含む実データを取得
"""
import os
import httpx
from typing import List, Optional
from app.models.schemas import FlightOffer, RawFlightData
from dotenv import load_dotenv

load_dotenv()


class FlightDataClient:
    """SerpApi を使用したフライトデータ取得クライアント"""
    
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY")
        self.use_mock = not self.api_key
        self.base_url = "https://serpapi.com/search"

    async def get_flight_offers(
        self, 
        departure: str, 
        arrival: str, 
        date: Optional[str] = None
    ) -> RawFlightData:
        """SerpApi (Google Flights) からオファーを取得"""
        if self.use_mock:
            return self._get_mock_data(departure, arrival, date)
        
        try:
            params = {
                "engine": "google_flights",
                "departure_id": departure,
                "arrival_id": arrival,
                "outbound_date": date if date else "2026-03-01",
                "currency": "JPY",
                "hl": "ja",
                "api_key": self.api_key,
                "type": "2"  # One-way
            }
            
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                return self._parse_serpapi_response(data)
        except Exception as e:
            print(f"SerpApi Error: {e}")
            return self._get_mock_data(departure, arrival, date)

    def _parse_serpapi_response(self, data: dict) -> RawFlightData:
        """SerpApi のレスポンスを共通モデルに変換"""
        offers = []
        
        # 'best_flights' と 'other_flights' から取得
        raw_flights = data.get("best_flights", []) + data.get("other_flights", [])
        
        for flight in raw_flights[:10]:  # 上位10件
            # flight['flights'] はセグメント（乗り継ぎ）のリスト
            segments = flight.get("flights", [])
            if not segments:
                continue
            
            first_seg = segments[0]
            last_seg = segments[-1]
            
            offers.append(FlightOffer(
                airline=first_seg.get("airline", "Unknown"),
                flight_number=first_seg.get("flight_number", "N/A"),
                departure_time=first_seg.get("departure_airport", {}).get("time", ""),
                arrival_time=last_seg.get("arrival_airport", {}).get("time", ""),
                price=float(flight.get("price", 0)),
                currency="JPY",
                booking_link=data.get("search_metadata", {}).get("google_flights_url")
            ))
            
        return RawFlightData(
            source="SerpApi (Google Flights)",
            offers=offers
        )

    def _get_mock_data(self, departure: str, arrival: str, date: str) -> RawFlightData:
        """APIキー未設定時のバックアップデータ"""
        return RawFlightData(
            source="SerpApi Mock (Google Flights 模倣)",
            offers=[
                FlightOffer(
                    airline="Peach",
                    flight_number="MM123",
                    departure_time="08:30",
                    arrival_time="10:00",
                    price=6500.0,
                    currency="JPY",
                    booking_link="https://www.google.com/travel/flights"
                ),
                FlightOffer(
                    airline="Jetstar Japan",
                    flight_number="GK456",
                    departure_time="12:00",
                    arrival_time="13:30",
                    price=7200.0,
                    currency="JPY",
                    booking_link="https://www.google.com/travel/flights"
                ),
                FlightOffer(
                    airline="Skymark",
                    flight_number="SKY789",
                    departure_time="15:00",
                    arrival_time="16:30",
                    price=9800.0,
                    currency="JPY",
                    booking_link="https://www.google.com/travel/flights"
                )
            ]
        )
