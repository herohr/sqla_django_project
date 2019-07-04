import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import InstrumentedAttribute

Base = declarative_base()


def now_time():
    return datetime.datetime.now()


class Serializer:
    def __init__(self, fields):
        self.fields = fields

    def model2dict(self, instance):
        _dict = {}
        none = object()
        for i in self.fields:
            val = getattr(instance, i, none)
            if val is none:
                raise ValueError("Instance {} has not attribute {}".format(instance, i))
            _dict[i] = val
        return _dict

    def qs2list(self, qs):
        _list = []
        for i in qs:
            _dict = self.model2dict(i)
            _list.append(_dict)
        return _list


class ModelBase(Base):
    __abstract__ = True
    serializer = Serializer([])

    def serialize(self):
        if not self.serializer.fields:
            raise NotImplementedError("Must to initial a serializer with fields in your model")

        return self.serializer.model2dict(self)


class User(ModelBase):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(64))
    password = Column(String(64))


class Article(ModelBase):
    __tablename__ = "article"

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(120))
    create_time = Column(DateTime, default=now_time)
    content = Column(Text)

    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship(User, backref="articles_of_user")

    serializer = Serializer(["id", "title", "create_time", "content", "author_id"])


def get_by_pk(session, model, pk):
    ins = session.query(model).filter_by(id=pk).one_or_none()
    return ins

# from blog.db import engine
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

