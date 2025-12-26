import json
import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

params: dict = {
    "apex": json.loads(os.getenv("PARAMETERS_APEX")),
    "enterprise": json.loads(os.getenv("PARAMETERS_ENTERPRISE")),
    "maestral": json.loads(os.getenv("PARAMETERS_MAESTRAL")),
    "proride": json.loads(os.getenv("PARAMETERS_PRORIDE")),
    "sparkle": json.loads(os.getenv("PARAMETERS_SPARKLE")),
    "tx": json.loads(os.getenv("PARAMETERS_TX")),
    "invoice": json.loads(os.getenv("PARAMETERS_INVOICE")),
    "peak": json.loads(os.getenv("PARAMETERS_PEAK")),
    "optima": json.loads(os.getenv("PARAMETERS_OPTIMA")),
    "eva": json.loads(os.getenv("PARAMETERS_EVA")),
    "xplore": json.loads(os.getenv("PARAMETERS_XPLORE")),
    "routemate": json.loads(os.getenv("PARAMETERS_RM"))
}


class DatabaseConnection:
    def __init__(self, **db_params):
        self.db_params = db_params
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = mysql.connector.connect(**self.db_params)
            self.cursor = self.connection.cursor(dictionary=True)
            return self.cursor

        except mysql.connector.Error as err:
            print(f"Failed to connect to mysql server: {err}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            if exc_type:
                self.connection.rollback()
                print(f"Transaction rolled back. Error: {exc_val}")
            else:
                self.connection.commit()

            self.cursor.close()
            self.connection.close()


def execute_query(_query: str, parameters: dict, insert_data: list[dict] | None = None):
    with DatabaseConnection(**parameters) as cursor:
        if not insert_data:
            cursor.execute(_query)
            result = cursor.fetchall()

            return result
        else:
            cursor.executemany(_query, insert_data)

            return f"Rows affected: {cursor.rowcount}"

