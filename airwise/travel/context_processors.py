from django.conf import settings


def api_keys(request):
    return {
        'openweather_api_key': getattr(settings, 'OPENWEATHER_API_KEY', ''),
    }
