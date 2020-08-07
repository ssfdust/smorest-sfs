"""测试ORM用例"""

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker

Base = declarative_base()

engine = create_engine("sqlite://")
Session_ = sessionmaker(bind=engine)
session: Session = Session_()


class Parent(Base):

    __tablename__ = "parents"

    id_ = Column("id", Integer, primary_key=True, autoincrement=True)

    name = Column(String)
    code = Column(String)

    children = relationship("Child", uselist=True)


class Child(Base):

    __tablename__ = "children"

    id_ = Column("id", Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, ForeignKey(Parent.id_))

    name_2 = Column(String)
    code_2 = Column(String)

    grand_children = relationship("GrandChild", uselist=True)


class GrandChild(Base):

    __tablename__ = "grand_children"

    id_ = Column("id", Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer, ForeignKey(Child.id_))

    name_3 = Column(String)


Base.metadata.create_all(engine)
