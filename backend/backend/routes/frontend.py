import os

from flask.wrappers import Request
from flask import send_from_directory
from werkzeug.datastructures import Headers

from backend import app
from backend.wrappers import auth


@app.route("/", methods=["GET", "POST"])
@app.route("/<path:path>", methods=["GET", "POST"])
@auth()
def frontend(req: Request, headers: Headers, path: str = "index.html"):
    return send_from_directory(
        os.path.join(os.getcwd(), "frontend", "out"),
        path
    )
