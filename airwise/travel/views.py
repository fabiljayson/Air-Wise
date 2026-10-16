import json
import logging

from django import forms
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .decorators import connexion_requise
from .forms import LoginForm, RegisterForm, FlightSearchForm
from .models import Utilisateur, Reservation
from .rate_limit import RateLimitMixin
from .services.amadeus_service import AmadeusService

logger = logging.getLogger(__name__)


def _user_context(request):
    """Return common template context for utilisateur state."""
    utilisateur = getattr(request, 'utilisateur', None)
    return {
        'utilisateur': utilisateur,
        'is_logged_in': bool(utilisateur),
    }


def home_view(request):
    return render(request, 'home.html', _user_context(request))


def about_view(request):
    return render(request, 'about.html', _user_context(request))


def services_view(request):
    return render(request, 'services.html', _user_context(request))


def contact_view(request):
    return render(request, 'contact.html', _user_context(request))


class ConnectionView(View, RateLimitMixin):
    rate_limit_key = 'login'
    rate_limit_count = 10
    rate_limit_window = 300

    def _get_client_ip(self, request):
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        return xff.split(',')[0].strip() if xff else request.META.get('REMOTE_ADDR', '')

    def get(self, request):
        return render(request, 'connection.html', {
            'login_form': LoginForm(),
            'register_form': RegisterForm(),
        })

    def post(self, request):
        if 'login' in request.POST:
            return self._handle_login(request)
        elif 'register' in request.POST:
            return self._handle_register(request)
        return render(request, 'connection.html', {
            'login_form': LoginForm(),
            'register_form': RegisterForm(),
        })

    def _handle_login(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            for error in form.errors.values():
                messages.error(request, error)
            return render(request, 'connection.html', {
                'login_form': form,
                'register_form': RegisterForm(),
            })

        ip = self._get_client_ip(request)
        if not self.check_rate_limit(ip):
            messages.error(request, 'Too many login attempts. Please try again later.')
            return render(request, 'connection.html', {
                'login_form': form,
                'register_form': RegisterForm(),
            })

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        try:
            utilisateur = Utilisateur.objects.get(email=email)
            if check_password(password, utilisateur.mot_de_passe):
                request.session.cycle_key()
                request.session['utilisateur_id'] = utilisateur.id
                request.session['utilisateur_nom'] = utilisateur.nomComplet
                request.session['utilisateur_email'] = utilisateur.email
                request.session['utilisateur_role'] = utilisateur.role
                logger.info('User %s logged in successfully', email)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                logger.warning('Failed login attempt for %s', email)
                messages.error(request, 'Incorrect email or password.')
        except Utilisateur.DoesNotExist:
            logger.warning('Login attempt for non-existent user %s', email)
            messages.error(request, 'Incorrect email or password.')

        return render(request, 'connection.html', {
            'login_form': form,
            'register_form': RegisterForm(),
        })

    def _handle_register(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            for error in form.errors.values():
                messages.error(request, error)
            return render(request, 'connection.html', {
                'login_form': LoginForm(),
                'register_form': form,
            })

        try:
            utilisateur = Utilisateur(
                nomComplet=form.cleaned_data['nom_complet'],
                email=form.cleaned_data['email'],
                telephone=form.cleaned_data.get('telephone', ''),
                mot_de_passe=make_password(form.cleaned_data['password']),
            )
            utilisateur.save()
            request.session.cycle_key()
            request.session['utilisateur_id'] = utilisateur.id
            request.session['utilisateur_nom'] = utilisateur.nomComplet
            request.session['utilisateur_email'] = utilisateur.email
            request.session['utilisateur_role'] = utilisateur.role
            logger.info('New user registered: %s', utilisateur.email)
            messages.success(request, 'Registration successful! Welcome!')
            return redirect('home')
        except Exception as e:
            logger.error('Registration error: %s', e)
            messages.error(request, 'An error occurred during registration.')

        return render(request, 'connection.html', {
            'login_form': LoginForm(),
            'register_form': form,
        })


connection_view = ConnectionView.as_view()


def deconnexion_view(request):
    user_email = request.session.get('utilisateur_email', 'unknown')
    request.session.flush()
    logger.info('User %s logged out', user_email)
    messages.success(request, 'Logged out successfully!')
    return redirect('connection')


@connexion_requise
def search_flights(request):
    if request.method != 'POST':
        return redirect('home')

    form = FlightSearchForm(request.POST)
    if not form.is_valid():
        messages.error(request, 'Please fill in all required fields correctly.')
        return redirect('home')

    origin = form.cleaned_data['departure'].strip()
    destination = form.cleaned_data['destination'].strip()
    departure_date = str(form.cleaned_data['departure_date'])
    passengers = form.cleaned_data['passagers']
    children = form.cleaned_data['children']
    flight_class = form.cleaned_data['flight_class']

    class_map = {
        'economique': 'ECONOMY',
        'business': 'BUSINESS',
        'premiere': 'FIRST',
    }
    travel_class = class_map.get(flight_class, 'ECONOMY')

    amadeus = AmadeusService()
    result = amadeus.search_flights(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        adults=max(int(passengers), 1),
        children=int(children),
        travel_class=travel_class,
    )

    if result is None:
        messages.error(request, 'Could not connect to the flight service. Please try again.')
        return redirect('home')

    if 'error' in result:
        messages.warning(request, result['error'])

    origin_label = origin.split(' - ')[1] if ' - ' in origin else origin
    dest_label = destination.split(' - ')[1] if ' - ' in destination else destination

    flights = result.get('flights', [])
    paginator = Paginator(flights, 10)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    ctx = _user_context(request)
    ctx.update({
        'flights': page_obj,
        'count': result.get('count', 0),
        'origin': origin_label,
        'destination': dest_label,
        'departure_date': departure_date,
        'passengers': passengers,
        'travel_class': travel_class.title(),
    })
    return render(request, 'search_results.html', ctx)


@csrf_exempt
@require_http_methods(["POST"])
def search_flights_ajax(request):
    """Public AJAX flight-search endpoint.

    Stateless (no session mutation, no auth required), so it is CSRF-exempt.
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    origin = data.get('origin', '').strip()
    destination = data.get('destination', '').strip()
    departure_date = data.get('departure_date', '').strip()
    passengers = data.get('passengers', 1)
    children = data.get('children', 0)
    travel_class = data.get('travel_class', 'ECONOMY')

    if not origin or not destination or not departure_date:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    try:
        passengers = max(int(passengers), 1)
        children = max(int(children), 0)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid passenger/child count'}, status=400)

    amadeus = AmadeusService()
    result = amadeus.search_flights(
        origin=origin,
        destination=destination,
        departure_date=departure_date,
        adults=passengers,
        children=children,
        travel_class=travel_class,
    )

    if result is None:
        return JsonResponse({'error': 'Could not connect to flight service'}, status=502)

    return JsonResponse(result)


@connexion_requise
def reserve_flight(request):
    if request.method != 'POST':
        return redirect('home')

    flight_id = request.POST.get('flight_id', '')
    flight_price = request.POST.get('flight_price', '0')
    origin = request.POST.get('origin', '')
    destination = request.POST.get('destination', '')
    departure_date = request.POST.get('departure_date', '')

    if not flight_id or not origin or not destination or not departure_date:
        messages.error(request, 'Missing reservation details. Please try again.')
        return redirect('home')

    try:
        price = float(flight_price)
    except (TypeError, ValueError):
        price = 0.0
    # Reject absurd prices defensively.
    if price < 0 or price > 1_000_000:
        messages.error(request, 'Invalid flight price.')
        return redirect('home')

    utilisateur = getattr(request, 'utilisateur', None)
    if not utilisateur:
        messages.error(request, 'Please log in to make a reservation.')
        return redirect('connection')

    user_instance = getattr(utilisateur, '_user', None) or utilisateur

    try:
        Reservation.objects.create(
            utilisateur=user_instance,
            flight_id=flight_id,
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            price=price,
            statut='Confirmed',
        )
    except Exception as e:  # noqa: BLE001 - surface any DB error to the user
        logger.error('Reservation creation failed for %s: %s', user_instance.email, e)
        messages.error(request, 'Could not create your reservation. Please try again.')
        return redirect('home')

    logger.info('Reservation created by %s: %s to %s', user_instance.email, origin, destination)
    messages.success(request, f'Reservation confirmed! Flight {origin} to {destination} on {departure_date} for {price:.2f} EUR.')
    return redirect('home')
