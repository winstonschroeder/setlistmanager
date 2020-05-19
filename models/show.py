from typing import List
from typing import Tuple
from datetime import date
from datetime import datetime

from models.base_model import BaseModel


class Show(BaseModel):
    show_date: date = None
    times: List[Tuple[datetime, datetime]] = []
    band: str = ''

    pass
