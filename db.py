from sqlalchemy import Boolean, Integer, String, create_engine, Column
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///jarvis.db")
Base = declarative_base()
_Session = sessionmaker(engine)

class Item(Base):
    __tablename__ = "itens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    num = Column(Integer)
    completed = Column(Boolean)

Base.metadata.create_all(engine)
