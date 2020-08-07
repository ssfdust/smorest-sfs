"""测试ORM用例"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_mptt import BaseNestedSets

Base = declarative_base()

engine = create_engine("sqlite://")
Session_ = sessionmaker(bind=engine)


class TestCodeTable(Base, BaseNestedSets):
    __tablename__ = "test_code_table"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=20), nullable=False)
    type_code = Column(String(length=20), nullable=False)
    value = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return self.name


class TestHierachyTable(Base, BaseNestedSets):
    __tablename__ = "test_hierachy_table"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=20), nullable=False)
    value = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return self.name


Base.metadata.create_all(engine)
