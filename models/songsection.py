from models.base_model import BaseModel
# from sqlalchemy import Column, String
from setlistmanager.db import Base



class SongSection(BaseModel, Base):
    __tablename__ = 'sonsections'
    pass
