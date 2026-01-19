"""
外部フライトデータクライアント
Amadeus API 等からのデータ取得を処理
"""
import os
from typing import List, Optional
from app.models.schemas import FlightOffer, RawFlightData
from dotenv import load_dotenv

load_dotenv()


class FlightDataClient:
    """外部フライトデータ取得クライアント"""
    
    def __init__(self):
        self.amadeus_api_key = os.getenv("AMADEUS_API_KEY")
        self.amadeus_api_secret = os.getenv("AMADEUS_API_SECRET")
        self.use_mock = not (self.amadeus_api_key and self.amadeus_api_secret)

    async def get_flight_offers(
        self, 
        departure: str, 
        arrival: str, 
        date: Optional[str] = None
    ) -> RawFlightData:
        """フライトオファーを取得"""
        if self.use_mock:
            return self._get_mock_data(departure, arrival, date)
        
        # TODO: 実装（Amadeus API 呼び出し）
        return self._get_mock_data(departure, arrival, date)

    def _get_mock_data(self, departure: str, arrival: str, date: str) -> RawFlightData:
        """開発用のモックデータ"""
        return RawFlightData(
            source="Amadeus Mock",
            offers=[
                FlightOffer(
                    airline="Japan Airlines",
                    flight_number="JL123",
                    departure_time="10:00",
                    arrival_time="11:30",
                    price=15000.0,
                    currency="JPY",
                    booking_link="https://www.jal.co.jp/"
                ),
                FlightOffer(
                    airline="ANA",
                    flight_number="NH456",
                    departure_time="14:00",
                    arrival_time="15:30",
                    price=22000.0,
                    currency="JPY",
                    booking_link="https://www.ana.co.jp/"
                ),
                FlightOffer(
                    airline="Peach",
                    flight_number="MM789",
                    departure_time="18:00",
                    arrival_time="19:30",
                    price=8500.0,
                    currency="JPY",
                    booking_link="https://www.flypeach.com/"
                )
            ]
        )
