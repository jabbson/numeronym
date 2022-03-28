# Write a function that can determine if a word is a numeronym and it is unique.

from typing import List
from unittest import mock
from unittest.mock import mock_open
import pytest


class InvalidNumeronym(Exception):
    pass


class NoNumeronym(Exception):
    pass


class NoWord(Exception):
    pass

def check_num(num: str, word: str) -> bool:
    num = num.lower()
    word = word.lower()

    # first and last letters must match
    if num[0] != word[0] or num[-1] != word[-1]:
        return False

    try:
        n = int(num[1:-1])
    except:
        raise InvalidNumeronym

    # num != letter count in the word
    if len(word[1:-1]) != n:
        return False

    return True


def check_num_list(num: str, word: str) -> bool:

    lst = get_data('/usr/share/dict/words')

    # no numeronym
    if len(num) == 0:
        raise NoNumeronym

    # numeronym is too short
    if len(num) == 1:
        raise InvalidNumeronym

    # numeronym starts or ends with a number
    if num[0].isnumeric() or num[-1].isnumeric():
        raise InvalidNumeronym

    # empty word
    if len(word) == 0:
        raise NoWord

    # two letter words
    if len(num) == 2 and num == word:
        raise True

    # empty list
    if not lst:
        return False

    # no work in the list
    if word not in lst:
        return False

    if not check_num(num, word):
        return False

    # iter list
    for w in lst:
        # skip the original word
        if w == word or len(w) == 0:
            continue

        # if other word matches too - ret False
        if check_num(num, w):
            return False

    return True

data = '''azoisobutyronitrile
katharometer
kotharometer'''

mopen = mock_open(read_data=data)

def get_data(filename: str) -> List[str]:
    with mock.patch('builtins.open', mopen):
        with open(filename) as f:
            return f.read().split('\n')


@pytest.mark.parametrize(
    "in1, in2, out",
    [
        # Everything works!
        ('a17e', 'azoisobutyronitrile', True),
        # Duplicate name in inputs!
        ('k10r', 'katharometer',        False),
        # Name isn't in the list!
        ('q10g', 'qwertyasdfzg',        False),
    ]
)
def test_check_num2(in1, in2, out):
    assert check_num_list(in1, in2) == out


@pytest.mark.parametrize(
    "in1, in2, exp",
    [
        ('k9',  'kubernetes', pytest.raises(InvalidNumeronym)),
        ('',    'kubernetes', pytest.raises(NoNumeronym)),
        ('k8s', '',           pytest.raises(NoWord)),
    ]
)
def test_check_num2_throws(in1, in2, exp):
    with exp:
        assert check_num_list(in1, in2) is not None


if __name__ == "__main__":
    # print(check_num2('a17e', 'azoisobutyronitrile', ['azoisobutyronitrile',  'cats', 'dogs']))
    pass
