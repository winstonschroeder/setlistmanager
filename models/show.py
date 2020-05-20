from typing import List
from typing import Tuple
from datetime import date
from datetime import datetime

from models.base_model import BaseModel
from sqlalchemy import Column, Integer, String, Date
from setlistmanager.db import Base

class Show(BaseModel, Base):
    __tablename__ = 'shows'
    show_date: date = None
    times: List[Tuple[datetime, datetime]] = []
    band: str = ''
    test = ['a', 'b', 'c']
    test2 = 'Get me'

    pass
