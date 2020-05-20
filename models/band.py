from models.base_model import BaseModel
from sqlalchemy import Column, String
from setlistmanager.db import Base


class Band(BaseModel, Base):
    __tablename__ = 'bands'
    pass
