import pytest

from twelve_tone.composer import Composer


# Parametrize fixture to test against all 12! rows?
@pytest.fixture
def tone_row():
    row = [3, 1, 9, 5, 4, 6, 8, 7, 12, 10, 11, 2]
    return row


@pytest.mark.skip
def test_get_tone_row(tone_row):
    m = Composer(tone_row=tone_row)
    row = m.tone_row
    assert list(row) == list(m.matrix[1])
    # col = m.get_tone_row(0, 1)
    # assert (list(col) == list(m.matrix[:, 1])


def test_top_row(tone_row):
    m = Composer(tone_row=tone_row)
    # check top row is unique
    duplicate_val = False
    if len(m.matrix[0]) > len(set(m.matrix[0])):
        duplicate_val = True
    assert duplicate_val is False
    assert len(m.matrix[0]) == 12


def test_translate_pitch():
    cell = 3
    pitch = Composer().to_sharp(cell)
    assert pitch == "D♯"


def test_master(tone_row):
    m = Composer(tone_row=tone_row)
    assert m.matrix[0][0] == 3
    assert m.matrix[11][0] == 4
    assert m.matrix[0][11] == 2
    assert m.matrix[11][11] == 3
    # check for 3s all the way diagonal
    for x in range(0, 12):
        assert m.matrix[x][x] == 3
