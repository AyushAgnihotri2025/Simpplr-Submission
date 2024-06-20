import jwt
from flask import request
from functools import wraps

from backend import app


def auth(
    check_auth: bool = False
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            req = request
            headers = req.headers
            if check_auth:
                token = req.headers.get("Authorization", "Bearer ").split(" ", 1)[1]
                try:
                    jwt.decode(token, app.secret_key, algorithms=["HS256"])
                except jwt.ExpiredSignatureError:
                    return dict(
                        success=False,
                        message="Session expired. Please log in again."
                    ), 401
                except jwt.InvalidTokenError:
                    return dict(
                        success=False,
                        message="Session expired. Please log in again."
                    ), 401
            return func(req, headers, *args, **kwargs)

        return wrapper

    return decorator
