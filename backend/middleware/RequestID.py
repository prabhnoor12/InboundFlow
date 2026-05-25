"""
Request ID Middleware for FastAPI.
Adds a unique X-Request-ID header to every response and makes it available in request.state for logging/debugging.
Usage:
    from backend.middleware.RequestID import RequestIDMiddleware
    app.add_middleware(RequestIDMiddleware)
"""

import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class RequestIDMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, header_name: str = "X-Request-ID"):
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(self, request: Request, call_next):
        # Use incoming request ID if present, else generate a new one
        request_id = request.headers.get(self.header_name)
        if not request_id:
            request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response: Response = await call_next(request)
        response.headers[self.header_name] = request_id
        return response
