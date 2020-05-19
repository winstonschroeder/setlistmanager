from typing import List
from models.base_model import BaseModel
from models.show import Show
from models.song import Song


class Setlist(BaseModel):
    songs: List[Song] = []
    show: Show = None

    def append_song(self, song: Song):
        self.songs.append(song)

    def move_song(self, song: Song, move_before: Song):
        if song not in self.songs:
            return
        if move_before not in self.songs:
            return

        self.songs.remove(song)
        idx = self.get_song_index(move_before)
        self.songs.insert(idx, song)

    def get_song_index(self, song: Song) -> int:
        return self.songs.index(song)
