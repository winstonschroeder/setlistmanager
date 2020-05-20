import jsons
from sqlalchemy import Column, Integer, String


class BaseModel(object):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name: str = ''):
        self.name = name

    def __repr__(self):
        return '%s' % self.name

    def payload(self):
        return jsons.dump(self, strip_privates=True)
