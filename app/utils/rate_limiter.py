import time
from fastapi import Request, HTTPException
from app.core.config import settings

# In-memory store (simple for task)
request_log = {}


def rate_limiter(request: Request):
    """
    Limits requests to 1 per X seconds per IP.
    Disabled when DISABLE_RATE_LIMIT is True.
    """
    if settings.DISABLE_RATE_LIMIT:
        return

    client_ip = request.client.host
    current_time = time.time()

    last_request_time = request_log.get(client_ip)

    if last_request_time:
        if current_time - last_request_time < settings.RATE_LIMIT_SECONDS:
            raise HTTPException(status_code=429, detail="Too many requests")

    request_log[client_ip] = current_time
