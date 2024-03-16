from app.config import settings
from app.database import sessionmanager


DATABASE_URL = settings.db_url if not settings.testing else settings.db_url_test

sessionmanager.init(DATABASE_URL)
