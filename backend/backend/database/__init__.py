import sqlite3
from sqlite3 import Connection

import psycopg2
from psycopg2._psycopg import connection

from backend import (
    DB_NAME, DB_HOST, DB_USER,
    DB_PASS, DB_PORT, LOCAL_DB,
    DEBUG,
)

conn = None

if not DEBUG:
    conn = psycopg2.connect(
        database=DB_NAME,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
    )

local_conn = sqlite3.connect(
    LOCAL_DB,
    check_same_thread=False
)
local_conn.row_factory = sqlite3.Row


def get_connection(is_prod: bool = False) -> connection | Connection:
    """
    Returns a database connection based on the environment.

    Args:
        is_prod (bool): A flag to determine the environment.
                        - If True, returns a PostgresSQL connection (production).
                        - If False, returns a SQLite connection (local/development).

    :param is_prod: A flag to determine the environment.
    :return: connection | Connection: A database connection object, either PostgresSQL or SQLite.
    """
    global local_conn

    if is_prod:
        return conn
    else:
        try:
            tempCur = local_conn.cursor()
            tempCur.close()
            return local_conn
        except sqlite3.ProgrammingError:
            local_conn = sqlite3.connect(
                LOCAL_DB,
                check_same_thread=False
            )
            local_conn.row_factory = sqlite3.Row
            return local_conn
