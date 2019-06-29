from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine
from django.conf import settings

db_url = settings.DB_URL
engine = create_engine(db_url)
Session = sessionmaker(engine)

__all__ = ["Session"]
