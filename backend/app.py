# FastAPI application setup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import auth_routes
from backend.middleware.ratelimiter import add_rate_limiter

app = FastAPI(title="InboundFlow API")

# CORS middleware (customize origins as needed)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # Change to specific domains in production
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Rate limiter middleware
add_rate_limiter(app)

# Request ID middleware (placeholder, implement if needed)
# from backend.middleware.RequestID import ...
# app.add_middleware(RequestIDMiddleware)

# Include authentication routes
app.include_router(auth_routes.router)
