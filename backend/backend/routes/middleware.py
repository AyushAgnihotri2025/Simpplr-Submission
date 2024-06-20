import datetime

from backend import app, __version__


@app.after_request
def add_cors(response):
    response.headers["X-Frame-Options"] = "DENY"  # SAMEORIGIN
    response.headers["X-App-Version"] = f"v{__version__}"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Date"] = datetime.datetime.now(tz=datetime.timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')

    if app.debug:
        response.headers["Access-Control-Expose-Headers"] = "Date, X-App-Version"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        response.headers["Access-Control-Max-Age"] = "10"
    return response
