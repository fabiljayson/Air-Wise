import json
from unittest.mock import patch, MagicMock

import requests as requests_lib
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from .models import Utilisateur, Reservation
from .middleware import LazyUser, AuthenticationMiddleware
from .services.amadeus_service import AmadeusService


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')


class AboutViewTest(TestCase):
    def test_about_status_code(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)


class ServicesViewTest(TestCase):
    def test_services_status_code(self):
        response = self.client.get(reverse('services'))
        self.assertEqual(response.status_code, 200)


class ContactViewTest(TestCase):
    def test_contact_status_code(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)


class ConnectionViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_connection_get(self):
        response = self.client.get(reverse('connection'))
        self.assertEqual(response.status_code, 200)

    def test_register_success(self):
        response = self.client.post(reverse('connection'), {
            'register': 'true',
            'nom_complet': 'Test User',
            'email': 'test@example.com',
            'telephone': '+1234567890',
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Utilisateur.objects.filter(email='test@example.com').exists())

    def test_register_password_mismatch(self):
        response = self.client.post(reverse('connection'), {
            'register': 'true',
            'nom_complet': 'Test User',
            'email': 'test2@example.com',
            'password': 'password123',
            'confirm_password': 'differentpassword',
        })
        self.assertEqual(response.status_code, 200)

    def test_register_duplicate_email(self):
        Utilisateur.objects.create(
            nomComplet='Existing User',
            email='dup@example.com',
            mot_de_passe=make_password('password123'),
        )
        response = self.client.post(reverse('connection'), {
            'register': 'true',
            'nom_complet': 'New User',
            'email': 'dup@example.com',
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        Utilisateur.objects.create(
            nomComplet='Login User',
            email='login@example.com',
            mot_de_passe=make_password('password123'),
        )
        response = self.client.post(reverse('connection'), {
            'login': 'true',
            'email': 'login@example.com',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_wrong_password(self):
        Utilisateur.objects.create(
            nomComplet='Login User',
            email='login2@example.com',
            mot_de_passe=make_password('password123'),
        )
        response = self.client.post(reverse('connection'), {
            'login': 'true',
            'email': 'login2@example.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Utilisateur.objects.create(
            nomComplet='Logout User',
            email='logout@example.com',
            mot_de_passe=make_password('password123'),
        )

    def test_logout_redirects(self):
        self.client.post(reverse('connection'), {
            'login': 'true',
            'email': 'logout@example.com',
            'password': 'password123',
        })
        response = self.client.get(reverse('deconnexion'))
        self.assertEqual(response.status_code, 302)


class SearchFlightsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Utilisateur.objects.create(
            nomComplet='Search User',
            email='search@example.com',
            mot_de_passe=make_password('password123'),
        )
        self.client.post(reverse('connection'), {
            'login': 'true',
            'email': 'search@example.com',
            'password': 'password123',
        })

    def test_search_get_redirects(self):
        response = self.client.get(reverse('search_flights'))
        self.assertEqual(response.status_code, 302)

    @patch('travel.views.AmadeusService')
    def test_search_post_with_results(self, MockAmadeus):
        mock_service = MockAmadeus.return_value
        mock_service.search_flights.return_value = {
            'flights': [{'id': '1', 'price': 300, 'currency': 'EUR', 'airline': 'AF',
                         'outbound': [], 'inbound': [], 'stops': 0,
                         'duration_out': 'PT2H', 'duration_back': '',
                         'travel_class': 'ECONOMY'}],
            'count': 1,
        }
        response = self.client.post(reverse('search_flights'), {
            'departure': 'CDG - Paris',
            'destination': 'DLA - Douala',
            'departure_date': '2025-12-25',
            'passagers': '1',
            'children': '0',
            'flight_class': 'economique',
        })
        self.assertIn(response.status_code, [200, 302])

    def test_search_post_missing_fields(self):
        response = self.client.post(reverse('search_flights'), {
            'departure': '',
            'destination': '',
            'departure_date': '',
        })
        self.assertEqual(response.status_code, 302)


class ReserveFlightViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Utilisateur.objects.create(
            nomComplet='Reserve User',
            email='reserve@example.com',
            mot_de_passe=make_password('password123'),
        )
        self.client.post(reverse('connection'), {
            'login': 'true',
            'email': 'reserve@example.com',
            'password': 'password123',
        })

    def test_reserve_creates_booking(self):
        response = self.client.post(reverse('reserve_flight'), {
            'flight_id': '12345',
            'flight_price': '450.00',
            'origin': 'Paris',
            'destination': 'Douala',
            'departure_date': '2025-12-25',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.first()
        self.assertEqual(reservation.origin, 'Paris')
        self.assertEqual(reservation.statut, 'Confirmed')

    def test_reserve_get_redirects(self):
        response = self.client.get(reverse('reserve_flight'))
        self.assertEqual(response.status_code, 302)


class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create(
            nomComplet='Test User',
            email='test@example.com',
            mot_de_passe=make_password('password123'),
        )

    def test_create_reservation(self):
        reservation = Reservation.objects.create(
            utilisateur=self.user,
            flight_id='12345',
            origin='Paris',
            destination='Douala',
            departure_date='2025-12-25',
            price=450.00,
            statut='Confirmed',
        )
        self.assertEqual(reservation.origin, 'Paris')
        self.assertEqual(reservation.statut, 'Confirmed')
        self.assertEqual(str(reservation), f'Reservation {self.user} - Paris to Douala')


class LazyUserTest(TestCase):
    def setUp(self):
        self.user = Utilisateur.objects.create(
            nomComplet='Lazy User',
            email='lazy@example.com',
            mot_de_passe=make_password('password123'),
        )

    def test_lazy_user_loads_from_session(self):
        request = MagicMock()
        request.session = {'utilisateur_id': self.user.id}
        lazy = LazyUser(request)
        self.assertTrue(bool(lazy))
        self.assertEqual(lazy.nomComplet, 'Lazy User')

    def test_lazy_user_none_when_no_session(self):
        request = MagicMock()
        request.session = {}
        lazy = LazyUser(request)
        self.assertFalse(bool(lazy))

    def test_lazy_user_none_when_invalid_id(self):
        request = MagicMock()
        request.session = {'utilisateur_id': 99999}
        lazy = LazyUser(request)
        self.assertFalse(bool(lazy))


class AmadeusServiceTest(TestCase):
    def test_extract_iata_with_dash(self):
        result = AmadeusService.extract_iata('CDG - Charles de Gaulle')
        self.assertEqual(result, 'CDG')

    def test_extract_iata_without_dash(self):
        result = AmadeusService.extract_iata('CDG')
        self.assertEqual(result, 'CDG')

    def test_extract_iata_empty(self):
        result = AmadeusService.extract_iata('')
        self.assertEqual(result, '')

    @patch('travel.services.amadeus_service.requests.post')
    def test_get_auth_token_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': 1799,
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        service = AmadeusService()
        token = service.get_auth_token()
        self.assertEqual(token, 'test_token')

    @patch('travel.services.amadeus_service.requests.post')
    def test_get_auth_token_failure(self, mock_post):
        mock_post.side_effect = requests_lib.exceptions.ConnectionError('Connection error')
        service = AmadeusService()
        token = service.get_auth_token()
        self.assertIsNone(token)

    @patch('travel.services.amadeus_service.requests.get')
    @patch.object(AmadeusService, '_headers')
    def test_search_flights_returns_results(self, mock_headers, mock_get):
        mock_headers.return_value = {'Authorization': 'Bearer test'}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': [{
                'id': '1',
                'price': {'total': '300', 'currency': 'EUR'},
                'itineraries': [{
                    'duration': 'PT2H',
                    'segments': [{
                        'departure': {'iataCode': 'CDG', 'at': '2025-12-25T10:00:00'},
                        'arrival': {'iataCode': 'DLA', 'at': '2025-12-25T16:00:00'},
                        'carrierCode': 'AF',
                        'number': '123',
                        'aircraft': {'code': 'B737'},
                    }]
                }],
                'travelerPricings': [{'fareDetailsBySegment': [{'cabin': 'ECONOMY'}]}],
            }]
        }
        mock_get.return_value = mock_response

        service = AmadeusService()
        result = service.search_flights('CDG', 'DLA', '2025-12-25')
        self.assertIsNotNone(result)
        self.assertEqual(result['count'], 1)
