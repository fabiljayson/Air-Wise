from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('contact/', views.contact_view, name='contact'),
    path('connection/', views.connection_view, name='connection'),
    path('deconnexion/', views.deconnexion_view, name='deconnexion'),
    path('search/', views.search_flights, name='search_flights'),
    path('api/search/', views.search_flights_ajax, name='search_flights_ajax'),
    path('reserve/', views.reserve_flight, name='reserve_flight'),
]
