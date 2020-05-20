from sqlalchemy import Column, String

from models.base_model import BaseModel
from setlistmanager.db import Base


class User(BaseModel, Base):
    __tablename__ = 'user'
    password: str = Column(String(20))
