import random
from itertools import pairwise
from functools import lru_cache
from typing import List

from rich.console import Console
from rich.text import Text

TwelveToneRow = List[int]
TwelveToneRowIntervals = List[int]
TwelveToneMatrix = List[TwelveToneRow]
SharpTone = str
FlatTone = str
MidiNote = int
Tone = int


class Composer:
    def __init__(self, tone_row: TwelveToneRow = None):
        if tone_row is None:
            self.tone_row = self.generate_tone_row()
        else:
            self.tone_row = tone_row
        self.matrix: TwelveToneMatrix = []
        self._generate_twelve_tone_matrix()

    def print_matrix_rows(self) -> None:
        for tone_row in self.matrix:
            for tone in tone_row:
                print(tone, end=" ")
            print()

    def print_tone_row(
        self, accidentals: str = "sharps", text_color: str = "cornsilk1"
    ) -> None:
        console = Console()
        for tone in self.get_melody():
            if accidentals == "sharps":
                tone_row = Text(self.to_sharp(tone))
            elif accidentals == "flats":
                tone_row = Text(self.to_flat(tone))
            tone_row.stylize(text_color, 0, 6)
            console.print(tone_row, end=" ")

    def generate_tone_row(self) -> TwelveToneRow:
        row = [tone for tone in range(12)]
        random.shuffle(row)
        return row

    @staticmethod
    def to_sharp(tone) -> SharpTone:
        accidentals_map = {
            0: "C",
            1: "C♯",
            2: "D",
            3: "D♯",
            4: "E",
            5: "F",
            6: "F♯",
            7: "G",
            8: "G♯",
            9: "A",
            10: "A♯",
            11: "B",
        }
        return accidentals_map[tone]

    @staticmethod
    def to_flat(tone) -> FlatTone:
        accidentals_map = {
            0: "C",
            1: "D♭",
            2: "D",
            3: "E♭",
            4: "E",
            5: "F",
            6: "G♭",
            7: "G",
            8: "A♭",
            9: "A",
            10: "B♭",
            11: "B",
        }
        return accidentals_map[tone]

    @staticmethod
    def to_midi(tone) -> MidiNote:
        midi_map = {
            0: 60,
            1: 61,
            2: 62,
            3: 63,
            4: 64,
            5: 65,
            6: 66,
            7: 67,
            8: 68,
            9: 69,
            10: 70,
            11: 71,
        }
        return midi_map[tone]

    def _generate_twelve_tone_matrix(self) -> None:
        def get_first_matrix_column() -> TwelveToneRow:
            return self.get_inversion_row(self.tone_row[0])

        for root in get_first_matrix_column():
            self.matrix.append(self.get_transposition(root))

    def get_inversion_row(self, root) -> TwelveToneRow:
        root = root % 12
        tone_row = [root]
        for interval in self.get_intervals_inverted():
            root = (root + interval) % 12
            tone_row.append(root)
        assert len(tone_row) == 12
        return tone_row

    def get_intervals_inverted(self) -> TwelveToneRowIntervals:
        intervals = []
        for i in self.get_intervals():
            intervals.append(-i)
        assert len(intervals) == 11
        return intervals

    def get_melody(self) -> TwelveToneRow:
        return random.choice(self.matrix)

    @lru_cache
    def get_intervals(self) -> TwelveToneRowIntervals:
        intervals = [y - x for (x, y) in pairwise(self.tone_row)]
        assert len(intervals) == 11
        return intervals

    def get_transposition(self, root) -> TwelveToneRow:
        root = root % 12
        tone_row = [root]
        for interval in self.get_intervals():
            root = (root + interval) % 12
            tone_row.append(root)
        assert len(tone_row) == 12
        return tone_row
