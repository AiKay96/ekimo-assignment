from dotenv import load_dotenv

from src.runner.config import settings

load_dotenv()
BASE_URL = settings.base_url
USERNAME = settings.username
PASSWORD = settings.password
