import unittest
import jsons
from unittest import TestCase
from models.setlist import Setlist
from models.song import Song


class Test(TestCase):
    def test_setlist(self):
        sl = Setlist("Selistname")
        sngs = [Song("Song 1"), Song("Song 2"), Song("Song 3")]
        try:

            for sng in sngs:
                sng.composer = "Mozart"
                sng.performer = "ABBA"
                sl.append_song(sng)
            self.assertEqual(len(sngs), len(sl.songs))
            idx = sl.get_song_index(sngs[2])
            self.assertIsNotNone(idx)
            print(idx)
            print(jsons.dump(sl))

            sl.move_song(sngs[2], sngs[0])
            sl.songs.remove(sngs[2])
            sl.move_song(sngs[2], sngs[1])
            print(jsons.dump(sl))

        except:
            self.fail()


if __name__ == "__main__":
    unittest.main()
