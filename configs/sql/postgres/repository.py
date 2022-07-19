# GLOBAL VARIABLES
ENV_FILE_NAME = ".env"

# HANDLING ENVIRONMENT VARIABLES
from dotenv import dotenv_values


def get_envs(_env_name: str) -> dict:
    config = dotenv_values(_env_name)

    if config==dict():
        raise NameError("Environment variables are being wrongly accessed!")

    return config

# HANDLING CONNECTION
import psycopg2

def process_env() -> dict:
    configs = get_envs(ENV_FILE_NAME)
    return {
        "host": configs["POSTGRES_HOST"],
        "database": configs["POSTGRES_DATABASE"],
        "user": configs["POSTGRES_USER"],
        "port": configs["POSTGRES_PORT"],
        "password": configs["POSTGRES_PASSWORD"]
    }

def get_connection():
    parameters = process_env()
    return psycopg2.connect(
        host=parameters.get("host"),
        dbname=parameters.get("database"),
        user=parameters.get("user"),
        password=parameters.get("password"),
        port=parameters.get("port")
    )