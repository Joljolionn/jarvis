from sqlalchemy import Boolean, Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import ConfigDict, BaseModel
from typing import Union


engine = create_engine("sqlite:///jarvis.db")
Base = declarative_base()
_Session = sessionmaker(engine)


class Item(Base):
    __tablename__ = "itens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    num = Column(Integer)
    completed = Column(Boolean)

class ItemResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    num: int
    completed: bool

class ItemTitleRequestDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str

class ItemIdRequestDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int

class ItemIdCompletedRequestDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    completed: bool

Base.metadata.create_all(engine)


def json_to_item(data: dict):
    return Item(
        id=data.get("id"),
        name=data.get("name"),
        num=data.get("num"),
        completed=data.get("completed"),
    )
