from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

metadata = MetaData()

engine = create_engine("sqlite://")
metadata.bind = engine

Session = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    nickname = Column(String)

    items = relationship("Item", uselist=True)

    def __repr__(self) -> str:
        return f"<User(name='{self.name}', nickname='{self.nickname}')>"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    uid = Column(Integer, ForeignKey("users.id"))

    def __repr__(self) -> str:
        return f"<Item(name={self.name})>"
