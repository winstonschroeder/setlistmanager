from datetime import datetime

from sqlalchemy import Column, String, Table, Integer, ForeignKey
from sqlalchemy.orm import relationship, mapper

from setlistmanager.db import Base


class Band(Base):
    pass


class Instrument(Base):
    pass


class Preset(Base):
    pass


class Setlist(Base):
    songs = relationship("Song", secondary="song2setlist")
    shows = relationship("Show", secondary="set")

    def append_song(self, song):
        self.songs.append(song)

    def move_song(self, song, move_before):
        if song not in self.songs:
            return
        if move_before not in self.songs:
            return

        self.songs.remove(song)
        idx = self.get_song_index(move_before)
        self.songs.insert(idx, song)

    def get_song_index(self, song) -> int:
        return self.songs.index(song)


class Show(Base):
    show_date = None
    setlist = relationship("Setlist", secondary="set")
    band: str = ''


class Song(Base):
    composer: str = Column(String(50))
    performer: str = Column(String(50))
    setlist = relationship("Setlist", secondary="song2setlist")


class SongSection(Base):
    pass


class Venue(Base):
    website: str = Column(String(80))
    location: str = Column(String(80))
    contact: str = Column(String(45))
    test: str = Column(String(50))


""" Relationships come here """

song2setlist = Table(
    "song2setlist",
    Base.metadata,
    Column('song_id', Integer, ForeignKey('song.id')),
    Column('setlist_id', Integer, ForeignKey('setlist.id')),
)

# class Set(Base):
#     song = Column('song_id', Integer, ForeignKey('song.id'))
#     show = Column('show_id', Integer, ForeignKey('show.id'), primaryjoin=lambda: Show.id==Set.show)
#     start = Column('start', DateTime)
#     end = Column('end', DateTime)

set = Table(
    "set",
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('show_id', Integer, ForeignKey('show.id')),
    Column('setlist_id', Integer, ForeignKey('setlist.id'))
)


class Set(object):
    show = None
    setlist = None
    start: datetime = None
    end: datetime = None


mapper(Set, set)
