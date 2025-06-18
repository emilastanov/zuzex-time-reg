from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv()

ENV = os.getenv("ENV")

TOKEN = os.getenv("BOT_TOKEN")
TOKEN_DEV = os.getenv("BOT_TOKEN_DEV")

DATABASE_URL = os.getenv("DATABASE_URL")

PAGINATION_PER_PAGE = os.getenv("PAGINATION_PER_PAGE", 5)
ADMIN_PASS_KEY = os.getenv("ADMIN_PASS_KEY", "5550123")

ZUZEX_BASE_URL = os.getenv("ZUZEX_BASE_URL")
