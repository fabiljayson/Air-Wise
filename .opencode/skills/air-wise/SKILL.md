---
name: air-wise
description: Air-Wise flight search work (Django 5.2 + Amadeus API + OpenWeather price prediction). Use for ANY task under /home/fabiljayson/Projects/Air-Wise — covers the nested-project layout, venv, and API-secret handling.
---

# Air-Wise

AI-assisted flight search and booking-time prediction: Amadeus Flight Search API (real-time flights) + OpenWeather (weather signals factored into price estimates), Django auth with rate-limited logins, per-user booking history, airport autocomplete.

## Layout & run

Django project sits **one level down** in `airwise/`; the venv sits at the repo root:

```bash
cd Air-Wise && source .venv/bin/activate && cd airwise && python manage.py runserver
```

## Non-negotiables

- `AMADEUS_*` and weather API keys live in environment/.env — **never commit secrets**, never hardcode the Amadeus test credentials.
- Keep the login rate-limiting intact (brute-force mitigation is a documented feature).
- Price prediction is heuristic/seasonal by design — label estimates as estimates in the UI; don't present them as guarantees.

## State

4 commits (last 2026-10-16), no tests yet, no CI. If asked to continue the project, propose adding pytest + a GitHub Actions workflow as the first step.
