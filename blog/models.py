import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


def now_time():
    return datetime.datetime.now()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(64))
    password = Column(String(64))


class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(120))
    create_time = Column(DateTime, default=now_time)
    content = Column(Text)

    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship(User, backref="articles_of_user")
#

# from blog.db import engine
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
