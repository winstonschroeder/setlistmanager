

from models.base_model import BaseModel


class Venue(BaseModel):
    website: str = ''
    location: str = ''
    contact: str = ''
    pass
