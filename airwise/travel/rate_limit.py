from django.core.cache import cache
from django.http import JsonResponse


class RateLimitMixin:
    """Rate limiter using Django cache backend."""

    rate_limit_key = 'default'
    rate_limit_count = 5
    rate_limit_window = 300  # seconds

    def check_rate_limit(self, identifier: str) -> bool:
        """Return True if request is allowed, False if rate limited."""
        key = f'ratelimit:{self.rate_limit_key}:{identifier}'
        attempts = cache.get(key, 0)
        if attempts >= self.rate_limit_count:
            return False
        cache.set(key, attempts + 1, self.rate_limit_window)
        return True

    def get_rate_limit_remaining(self, identifier: str) -> int:
        key = f'ratelimit:{self.rate_limit_key}:{identifier}'
        attempts = cache.get(key, 0)
        return max(0, self.rate_limit_count - attempts)
