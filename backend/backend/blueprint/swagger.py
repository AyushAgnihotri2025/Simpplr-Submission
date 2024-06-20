from backend import API_VERSION
from flask_swagger_ui import get_swaggerui_blueprint

API_URL = '/swagger.json'
SWAGGER_URL = f'/api/{API_VERSION}/docs'

# Call factory function to create our blueprint
swaggerUi_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Student Management"
    }
)
