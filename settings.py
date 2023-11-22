from environs import Env

env = Env()
env.read_env()

REGISTRATION = env.bool("REGISTRATION")

QUART_HOST = env.str("QUART_HOST")
QUART_PORT = env.int("QUART_PORT")
QUART_DEBUG = env.bool("QUART_DEBUG")
QUART_SECRET = env.str("QUART_SECRET")

DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_USER")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.int("DB_PORT")
DB_NAME = env.str("DB_NAME")
DB_DSN = f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

VERSION = "1.0.0"