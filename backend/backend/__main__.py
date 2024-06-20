import sys

from backend import (
    PORT,
    HOST,
    DEBUG,
)
from backend.routes import *
from backend.scripts import setup_db

if __name__ == '__main__':
    if len(sys.argv) > 1:
        task = sys.argv[1]

        match task:
            case 'setupDB':
                setup_db()
            case _:
                sys.exit("Invalid argument provided.")
    else:
        app.run(
            host=HOST,
            port=PORT,
            debug=DEBUG,
            load_dotenv=True,
        )
