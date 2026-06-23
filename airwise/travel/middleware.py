from typing import Any, Optional

from django.http import HttpRequest


class LazyUser:
    """Lazy-loading user proxy that defers DB query until attribute access."""

    def __init__(self, request: HttpRequest):
        self._request = request
        self._user: Optional[Any] = None
        self._loaded = False

    def _load(self) -> None:
        """Load the user from the session if not already loaded."""
        if not self._loaded:
            self._loaded = True
            user_id = self._request.session.get('utilisateur_id')
            if user_id:
                try:
                    from .models import Utilisateur
                    self._user = Utilisateur.objects.get(id=user_id)
                except Utilisateur.DoesNotExist:
                    self._user = None
                    for key in ['utilisateur_id', 'utilisateur_nom', 'utilisateur_email', 'utilisateur_role']:
                        if key in self._request.session:
                            del self._request.session[key]
            else:
                self._user = None

    def __getattr__(self, name: str) -> Any:
        self._load()
        if self._user is None:
            return None
        return getattr(self._user, name)

    def __bool__(self) -> bool:
        self._load()
        return self._user is not None


class AuthenticationMiddleware:
    """Middleware that attaches a lazy user proxy to each request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        request.utilisateur = LazyUser(request)
        response = self.get_response(request)
        return response
