from uuid import uuid4
from flask import Flask

from .config import *
from backend.blueprint import swaggerUi_blueprint, SWAGGER_URL

__version__ = '1.0.0'

app = Flask(
    __name__,
    static_url_path='',
    static_folder=os.path.join(os.path.dirname(__file__), 'static'),
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
)
app.debug = DEBUG
app.config['SECRET_KEY'] = str(uuid4())
app.register_blueprint(swaggerUi_blueprint, url_prefix=SWAGGER_URL)
