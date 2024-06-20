import jwt
import base64
from flask.wrappers import Request
from datetime import datetime, timedelta
from werkzeug.datastructures import Headers

from backend.wrappers import auth
from backend import app, API_VERSION


LOGIN_CREDS = {
    "username": ["admin"],
    "password": ["test@1234"],
}

@app.route(f"/api/{API_VERSION}/facultyLogin", methods=['POST'])
@auth()
def faculty_login(req: Request, headers: Headers):
    if not req.json:
        return dict(
            success=False,
            message='Invalid Request.',
        ), 400

    username, password = req.json.get("username"), req.json.get("password")

    if username and password:
        # TODO: Make a scalable and better login system.
        #       * Add DB + SignUp + Better Auth Tokens.
        if (
            username.lower() in LOGIN_CREDS["username"] and
            password in LOGIN_CREDS["password"] and
            LOGIN_CREDS["username"].index(username) == LOGIN_CREDS["password"].index(password)
        ):
            exp = datetime.now() + timedelta(hours=1)

            token = jwt.encode({
                'exp': exp,
                'username': username,
                'user_id': base64.b64encode(str(LOGIN_CREDS["username"].index(username)).encode()).decode(),
            }, app.secret_key, "HS256")

            return dict(
                token=token,
                success=True,
                message='Successfully logged in.',
            )

    return dict(
        success=False,
        message='Invalid Credentials.',
    ), 401
