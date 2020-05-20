from models.base_model import BaseModel
from sqlalchemy import Column, String
from setlistmanager.db import Base


class Song(BaseModel, Base):
    __tablename__ = 'songs'
    composer: str = Column(String(50))
    performer: str = Column(String(50))

    pass
