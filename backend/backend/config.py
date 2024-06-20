import os

PORT = os.environ.get("PORT", "8080")
HOST = os.environ.get("HOST", "0.0.0.0")
DEBUG = (os.environ.get("DEBUG", "true").lower() == "true")

os.makedirs(os.path.join(os.getcwd(), "db"), exist_ok=True)
LOCAL_DB = os.path.join(os.getcwd(), "db", os.environ.get('LOCAL_DB', 'students.db'))

DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')

API_VERSION = os.environ.get('API_VERSION', 'v1')
