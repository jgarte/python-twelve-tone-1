import random
from copy import deepcopy
from itertools import pairwise
from typing import List
from typing import Optional

import abjad
from rich.console import Console
from rich.table import Table


class Composer(object):
    def __init__(self, tone_row: Optional[List[int]] = None):
        if tone_row is None:
            self.tone_row = self.generate_tone_row()
        else:
            self.tone_row = tone_row
        self.matrix: List[List[int]] = []
        self.generate_twelve_tone_matrix()
        self.table = Table(title="Print Matrix P0 Horizontally")

    def print_matrix(self) -> None:
        for tone_row in self.matrix:
            print(tone_row)

    def play_tone_row(self) -> None:
        row = abjad.pcollections.TwelveToneRow(items=self.get_melody())
        abjad.persist.as_midi(row, "tone_row.midi")

    def print_matrix_rich(self) -> None:
        for row in self.matrix:
            # TODO: Support flats.
            self.table.add_row(*[str(tone) for tone in row])
        console = Console()
        console.print(self.table)

    def print_matrix_cli(self, accidentals: str = "sharps") -> None:
        for tone in self.get_melody():
            if accidentals == "sharps":
                print(self.to_sharp(tone), end=" ")
            elif accidentals == "flats":
                print(self.to_flat(tone), end=" ")

    def generate_tone_row(self) -> List[int]:
        row = [tone for tone in range(12)]
        random.shuffle(row)
        return row

    @staticmethod
    def to_sharp(tone) -> str:
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
    def to_flat(tone) -> str:
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
    def to_midi(tone) -> int:
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

    def generate_twelve_tone_matrix(self) -> List[List[int]]:
        tone_row = deepcopy(self.tone_row)
        tone_row.reverse()
        for tone in tone_row:
            self.matrix.append(self.get_transposition(tone))
        # put last element at the top
        self.matrix.insert(0, self.matrix.pop())
        return self.matrix

    def get_melody(self) -> List[int]:
        return random.choice(self.matrix)

    def get_intervals(self) -> List[int]:
        intervals = [y - x for (x, y) in pairwise(self.tone_row)]
        assert len(intervals) == 11
        return intervals

    def get_transposition(self, root) -> List[int]:
        root = root % 12
        tone_row = [root]
        for interval in self.get_intervals():
            root = (root + interval) % 12
            tone_row.append(root)
        assert len(tone_row) == 12
        return tone_row
