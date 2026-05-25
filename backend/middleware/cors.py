"""
Reusable CORS middleware setup for FastAPI.
Usage:
	from backend.middleware.cors import add_cors_middleware
	app = FastAPI()
	add_cors_middleware(app)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app: FastAPI, allow_origins=None, allow_credentials=True, allow_methods=None, allow_headers=None):
	"""
	Adds CORS middleware to the FastAPI app with default or custom settings.
	"""
	if allow_origins is None:
		allow_origins = ["*"]  # Change to specific domains in production
	if allow_methods is None:
		allow_methods = ["*"]
	if allow_headers is None:
		allow_headers = ["*"]
	app.add_middleware(
		CORSMiddleware,
		allow_origins=allow_origins,
		allow_credentials=allow_credentials,
		allow_methods=allow_methods,
		allow_headers=allow_headers,
	)
