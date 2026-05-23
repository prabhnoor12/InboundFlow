
"""
Rate Limiter Middleware for FastAPI using slowapi.
Usage:
    from backend.middleware.ratelimiter import add_rate_limiter
    app = FastAPI()
    add_rate_limiter(app)
    # Use @limiter.limit("10/minute") on routes for custom limits
"""

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request

# Create a Limiter instance with default settings (100 requests/minute per IP)
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

def add_rate_limiter(app: FastAPI):
    """
    Adds rate limiting middleware and exception handler to the FastAPI app.
    """
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.middleware('http')(limiter.middleware)

# Example usage for custom per-route limit:
# from backend.middleware.ratelimiter import limiter
# @app.get("/some-endpoint")
# @limiter.limit("10/minute")
# async def some_endpoint():
#     ...
