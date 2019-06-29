import sqlalchemy

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()  # 基类 （鸡肋）

engine = create_engine("sqlite:///db.sqlite3")
Session = sessionmaker(engine)


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20))
    age = Column(Integer)


# Base.metadata.create_all(engine)

session = Session()

# person = Person(name="NewPerson", age=12)
#
# session.add(person)
#
# session.commit()

qs = session.query(Person)
for i in qs:
    print(i.id, i.name, i.age)
