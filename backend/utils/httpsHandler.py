"""
HTTPSHandler Utility
-------------------
Ensures every request is made over HTTPS (htpx), with support for X-Forwarded-Proto header (for proxies) and development mode.

Usage:
	from backend.utils.httpsHandler import HTTPSHandler
    
	# As a dependency in FastAPI route
	@app.get("/secure-endpoint", dependencies=[Depends(HTTPSHandler.enforce_https)])
	async def secure_endpoint():
		...

	# As a decorator
	@HTTPSHandler.require_https
	async def secure_endpoint():
		...
"""

from fastapi import Request, HTTPException
import os
from functools import wraps

class HTTPSHandler:
	@staticmethod
	async def enforce_https(request: Request, allow_dev: bool = True):
		"""
		Enforce HTTPS for incoming requests.
		- Checks request.url.scheme
		- Checks X-Forwarded-Proto header (for proxies)
		- Allows HTTP in development if allow_dev is True and ENV=development
		"""
		# Allow HTTP in development mode
		if allow_dev and os.environ.get("ENV", "production").lower() == "development":
			return
		# Check X-Forwarded-Proto header (proxy support)
		xfp = request.headers.get("x-forwarded-proto")
		if xfp:
			if xfp.lower() != "https":
				raise HTTPException(status_code=403, detail="HTTPS required (proxy header).")
		elif request.url.scheme != "https":
			raise HTTPException(status_code=403, detail="HTTPS required.")

	@staticmethod
	def require_https(func=None, *, allow_dev: bool = True):
		"""
		Decorator to enforce HTTPS on FastAPI endpoints.
		Usage:
			@HTTPSHandler.require_https
			async def endpoint(request: Request): ...
		"""
		def decorator(f):
			@wraps(f)
			async def wrapper(*args, **kwargs):
				# Find Request in args or kwargs
				request = kwargs.get("request")
				if not request:
					for arg in args:
						if isinstance(arg, Request):
							request = arg
							break
				if not request:
					raise RuntimeError("Request object not found for HTTPS enforcement.")
				await HTTPSHandler.enforce_https(request, allow_dev=allow_dev)
				return await f(*args, **kwargs)
			return wrapper
		return decorator(func) if func else decorator
