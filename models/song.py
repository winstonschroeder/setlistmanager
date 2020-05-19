from models.base_model import BaseModel


class Song(BaseModel):
    composer: str = ''
    performer: str = ''

    pass
