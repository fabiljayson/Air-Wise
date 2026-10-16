# Air-Wise

Air-Wise is an AI-powered flight search and price-prediction web application. It combines real-time flight data from the Amadeus API with OpenWeather weather intelligence to help travelers find the best flight deals and predict the optimal time to book.

Built with Django 5.2 and a clean, responsive front-end.

## Features

- **Real-time flight search** powered by the Amadeus Flight Search API
- **AI price prediction** based on seasonal trends, demand, and weather signals
- **Weather intelligence** for destinations, factored into price estimates
- **User authentication** with registration, login, logout, and session management
- **Flight reservation** with per-user booking history
- **Rate limiting** on login attempts to mitigate brute force
- **Responsive UI** with airport autocomplete and interactive search controls

## Tech stack

| Layer | Technology |
| --- | --- |
| Backend | Django 5.2, Python 3.11+ |
| Flight data | Amadeus REST API (OAuth2 client-credentials) |
| Weather | OpenWeatherMap REST API |
| Front-end | Django templates, vanilla JS, Font Awesome, Google Fonts |
| Cache | Django in-memory cache (rate limiting) |
| Database | SQLite (default), ready for Postgres/MySQL swap |

## Project structure

```
Air-Wise/
├── airwise/                  # Django project package
│   ├── settings.py           # Configuration, security hardening
│   ├── urls.py               # Root URL configuration
│   ├── asgi.py / wsgi.py     # ASGI/WSGI entry points
│   └── manage.py             # Management CLI
├── travel/                   # Main Django app
│   ├── views.py              # View functions / class-based views
│   ├── models.py             # Domain models
│   ├── forms.py              # Form classes
│   ├── middleware.py         # Lazy user proxy
│   ├── decorators.py         # Login-required decorator
│   ├── rate_limit.py         # Rate-limit mixin
│   ├── services/
│   │   └── amadeus_service.py # Amadeus API client
│   ├── static/               # CSS, JS, images
│   └── templates/            # HTML templates
├── requirements.txt          # Pinned dependencies
├── .env.example              # Environment variable template
├── LICENSE
├── ARCHITECTURE.md
└── SECURITY.md
```

## Quick start

1. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env and fill in your Amadeus / OpenWeather keys
   ```

3. **Run the development server**

   ```bash
   cd airwise
   python manage.py migrate
   python manage.py runserver
   ```

4. **(Optional) Run the test suite**

   ```bash
   python manage.py test travel
   ```

## Environment variables

See `.env.example` for the full list. Key variables:

| Variable | Purpose |
| --- | --- |
| `DEBUG` | Enable Django debug mode (`True`/`False`) |
| `DJANGO_SECRET_KEY` | Django secret key (required in production) |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts |
| `AMADEUS_API_KEY` / `AMADEUS_API_SECRET` | Amadeus OAuth2 credentials |
| `AMADEUS_BASE_URL` | Amadeus base URL (defaults to test API) |
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key |
| `CSRF_TRUSTED_ORIGINS` | Trusted CSRF origins (production) |
| `SECURE_SSL_REDIRECT` | Redirect HTTP to HTTPS (production) |
| `SECURE_HSTS_SECONDS` | HSTS max-age in seconds (production) |
| `LOG_LEVEL` | Minimum log level (`INFO` default) |

## Production deployment

Air-Wise is designed to run behind a reverse proxy (nginx) or on a PaaS such as Fly.io, Render, or AWS Elastic Beanstalk.

Recommended production checklist:

- Set `DEBUG=False`
- Provide a strong `DJANGO_SECRET_KEY`
- Populate `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`
- Enable `SECURE_SSL_REDIRECT`, `SECURE_HSTS_*`, and secure cookies
- Use a production database (PostgreSQL recommended)
- Run `python manage.py collectstatic` and serve static files via your proxy
- Run Gunicorn behind a proxy, e.g.:

  ```bash
  gunicorn --workers 3 --bind 0.0.0.0:8000 airwise.wsgi:application
  ```

## Testing

The project ships with 27 Django tests covering views, models, middleware, and the Amadeus service. Run them with:

```bash
cd airwise
python manage.py test travel
```

## License

See [LICENSE](LICENSE) for details.

## Security

See [SECURITY.md](SECURITY.md) for reporting guidance and the project's security posture.