import logging
import os
import time
from typing import Any, Optional

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class AmadeusService:
    """Service for interacting with the Amadeus flight search API."""

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.api_key = api_key or settings.AMADEUS_API_KEY
        self.api_secret = api_secret or settings.AMADEUS_API_SECRET
        self.base_url = settings.AMADEUS_BASE_URL.rstrip('/')
        self.token: Optional[str] = None
        self.token_expiry: Optional[float] = None

    def get_auth_token(self) -> Optional[str]:
        """Get or refresh the OAuth2 bearer token from Amadeus."""
        if self.token and self.token_expiry and self.token_expiry > time.time():
            return self.token

        url = f"{self.base_url}/v1/security/oauth2/token"
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }

        try:
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            auth_data = response.json()
            self.token = auth_data['access_token']
            self.token_expiry = time.time() + auth_data['expires_in'] - 60
            logger.info('Amadeus auth token obtained successfully')
            return self.token
        except requests.exceptions.RequestException as e:
            logger.error('Amadeus auth error: %s', e)
            return None

    def _headers(self) -> Optional[dict[str, str]]:
        """Return authorization headers for API requests."""
        token = self.get_auth_token()
        if not token:
            return None
        return {'Authorization': f'Bearer {token}'}

    @staticmethod
    def extract_iata(input_str: str) -> str:
        """Extract IATA code from a string like 'CDG - Charles de Gaulle'."""
        if not input_str:
            return input_str
        if ' - ' in input_str:
            return input_str.split(' - ')[0].strip()
        return input_str.strip()

    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        adults: int = 1,
        children: int = 0,
        travel_class: str = 'ECONOMY',
    ) -> Optional[dict[str, Any]]:
        """Search for flights using the Amadeus API.

        Returns a dict with 'flights' list and 'count', or an 'error' key on failure.
        Returns None if authentication fails.
        """
        headers = self._headers()
        if not headers:
            return None

        origin_code = self.extract_iata(origin)
        dest_code = self.extract_iata(destination)

        url = f"{self.base_url}/v2/shopping/flight-offers"
        params = {
            'originLocationCode': origin_code,
            'destinationLocationCode': dest_code,
            'departureDate': departure_date,
            'adults': max(int(adults), 1),
            'children': int(children) if children else 0,
            'travelClass': travel_class.upper(),
            'currencyCode': 'EUR',
            'max': 20,
        }

        try:
            logger.info('Searching flights: %s -> %s on %s', origin_code, dest_code, departure_date)
            response = requests.get(url, headers=headers, params=params, timeout=15)
            if response.status_code == 200:
                result = self._parse_flights(response.json())
                logger.info('Found %d flights', result.get('count', 0))
                return result
            elif response.status_code == 400:
                return {'error': 'Invalid search parameters. Please check airport codes and dates.', 'flights': []}
            elif response.status_code == 429:
                return {'error': 'Too many requests. Please try again in a moment.', 'flights': []}
            else:
                return {'error': f'API error (status {response.status_code}).', 'flights': []}
        except requests.exceptions.Timeout:
            return {'error': 'Request timed out. Please try again.', 'flights': []}
        except requests.exceptions.RequestException as e:
            logger.error('Flight search network error: %s', e)
            return {'error': f'Network error: {str(e)}', 'flights': []}

    def _parse_flights(self, data: dict) -> dict[str, Any]:
        """Parse Amadeus API response into a simplified flight list."""
        flights = []
        for offer in data.get('data', []):
            price_info = offer.get('price', {})
            itineraries = offer.get('itineraries', [])

            segments_out = itineraries[0]['segments'] if len(itineraries) > 0 else []
            segments_back = itineraries[1]['segments'] if len(itineraries) > 1 else []

            flight = {
                'id': offer.get('id', ''),
                'price': float(price_info.get('total', 0)),
                'currency': price_info.get('currency', 'EUR'),
                'airline': segments_out[0].get('carrierCode', '') if segments_out else '',
                'outbound': self._parse_segments(segments_out),
                'inbound': self._parse_segments(segments_back),
                'stops': max(len(segments_out) - 1, 0),
                'duration_out': itineraries[0].get('duration', '') if itineraries else '',
                'duration_back': itineraries[1].get('duration', '') if len(itineraries) > 1 else '',
                'travel_class': offer.get('travelerPricings', [{}])[0].get('fareDetailsBySegment', [{}])[0].get('cabin', 'ECONOMY') if offer.get('travelerPricings') else 'ECONOMY',
            }
            flights.append(flight)

        flights.sort(key=lambda x: x['price'])
        return {'flights': flights, 'count': len(flights)}

    @staticmethod
    def _parse_segments(segments: list[dict]) -> list[dict[str, str]]:
        """Parse flight segments into a simplified format."""
        result = []
        for seg in segments:
            dep = seg.get('departure', {})
            arr = seg.get('arrival', {})
            result.append({
                'from': dep.get('iataCode', ''),
                'from_city': dep.get('terminal', ''),
                'to': arr.get('iataCode', ''),
                'to_city': arr.get('terminal', ''),
                'departure': dep.get('at', ''),
                'arrival': arr.get('at', ''),
                'carrier': seg.get('carrierCode', ''),
                'flight_number': seg.get('number', ''),
                'aircraft': seg.get('aircraft', {}).get('code', ''),
            })
        return result

    def predict_flight_price(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
    ) -> Optional[dict[str, Any]]:
        """Get price prediction metrics for a flight route."""
        headers = self._headers()
        if not headers:
            return None

        origin_code = self.extract_iata(origin)
        dest_code = self.extract_iata(destination)

        url = f"{self.BASE_URL}/v1/analytics/itinerary-price-metrics"
        params = {
            'originIataCode': origin_code,
            'destinationIataCode': dest_code,
            'departureDate': departure_date,
            'currencyCode': 'EUR',
            'oneWay': 'true' if not return_date else 'false'
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if 'data' in data and len(data['data']) > 0:
                price_metrics = data['data'][0].get('priceMetrics', {})
                return {
                    'minimum_price': price_metrics.get('minimum', {}).get('amount', 0),
                    'maximum_price': price_metrics.get('maximum', {}).get('amount', 0),
                    'average_price': price_metrics.get('average', {}).get('amount', 0),
                    'currency': price_metrics.get('currency', 'EUR')
                }
            return None
        except requests.exceptions.RequestException as e:
            logger.error('Price prediction error: %s', e)
            return None
