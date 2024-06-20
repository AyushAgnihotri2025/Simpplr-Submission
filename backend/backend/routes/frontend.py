import os

from flask import send_file
from flask.wrappers import Request
from werkzeug.datastructures import Headers

from backend import app
from backend.wrappers import auth


@app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
@app.route("/dashboard/search", defaults={"path": "dashboard/search"}, methods=["GET", "POST"])
@app.route("/dashboard/search/", defaults={"path": "dashboard/search"}, methods=["GET", "POST"])
@app.route("/dashboard/getall", defaults={"path": "dashboard/getall"}, methods=["GET", "POST"])
@app.route("/dashboard/getall/", defaults={"path": "dashboard/getall"}, methods=["GET", "POST"])
@auth()
def homePage(req: Request, headers: Headers, path: str):
    return send_file(
        os.path.join(app.static_folder, path, "index.html")
    )

@app.errorhandler(404)
def page_not_found(e):
    return send_file(os.path.join(app.static_folder, "404.html")), 404
