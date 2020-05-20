from models.base_model import BaseModel
from sqlalchemy import Column, String
from setlistmanager.db import Base

class Venue(BaseModel, Base):
    __tablename__ = 'venues'
    website: str = Column(String(80))
    location: str = Column(String(80))
    contact: str = Column(String(45))
    test: str = Column(String(50))
    pass
