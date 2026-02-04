from environs import Env

env = Env()
env.read_env(path='.env')

BOT_TOKEN = env.str("BOT_TOKEN")
DEVELOPER_ID = env.str("DEVELOPER_ID")

DB_NAME = env.str("DB_NAME")
DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")

DB_CONFIG = {
    "database": DB_NAME,
    "user": DB_USER,
    "port": DB_PORT,
    "host": DB_HOST,
    "password": DB_PASS
}
