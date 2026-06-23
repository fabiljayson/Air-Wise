import os
from dotenv import load_dotenv

load_dotenv()


def api_keys(request):
    return {
        'openweather_api_key': os.getenv('OPENWEATHER_API_KEY', ''),
    }
