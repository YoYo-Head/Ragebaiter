from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler
from fastapi import Request, Header, HTTPException

import os
import secrets
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("API_KEY")

def real_ip(request: Request):
    forwarded = request.headers.get("X-Forwarded-For")

    if forwarded:
        return forwarded.split(",")[0]

    return request.client.host


async def verify_api_key(x_api_key: str = Header(default=None)):
    if key is None:
        raise HTTPException(status_code=500, detail="Shhhh!!! Don't talk abt this. BTW, u should let the dev know abt this :)")
    
    elif x_api_key != key:
        raise HTTPException(status_code=401, detail="Permission denined :(. Check if you inputted the key right.")



limiter = Limiter(key_func=real_ip)#, default_limits=["30/minute"])