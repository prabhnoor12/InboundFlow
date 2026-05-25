# FastAPI application setup
from fastapi import FastAPI
from backend.middleware.cors import add_cors_middleware
from backend.routes import auth_routes
from backend.middleware.ratelimiter import add_rate_limiter

app = FastAPI(title="InboundFlow API")

# CORS middleware (customize origins as needed)
add_cors_middleware(app)

# Rate limiter middleware
add_rate_limiter(app)

# Request ID middleware for tracking/debugging
from backend.middleware.RequestID import RequestIDMiddleware
app.add_middleware(RequestIDMiddleware)

# Include authentication routes
app.include_router(auth_routes.router)
