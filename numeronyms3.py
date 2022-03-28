# Write a function that can determine if a word is a numeronym and it is unique.

from typing import List
from unittest import mock
from unittest.mock import mock_open
import pytest
from itertools import groupby

class InvalidNumeronym(Exception):
    pass


class NoNumeronym(Exception):
    pass


class NoWord(Exception):
    pass

def check_num(num: str, word: str) -> bool:
    num = num.lower()
    word = word.lower()

    word_pointer = 0

    # 'c12u2r22' --> ['c', '12', 'u', '2', 'r', '22']
    for _, v in groupby(num, lambda x: x.isalpha()):
        next_num_val = ''.join(v)

        if next_num_val.isalpha():
            if word[word_pointer] == next_num_val:
                word_pointer += 1
                continue
            return False
        elif next_num_val.isnumeric():
            next_num_val_num = int(next_num_val)
            # dont have enough letters in word to advance
            if word_pointer + next_num_val_num > len(word):
                return False
            word_pointer += next_num_val_num
        else:
            raise InvalidNumeronym

    if word_pointer < len(word):
        return False

    return True


def check_num_list(num: str, word: str) -> bool:

    lst = get_data('/usr/share/dict/words')

    # no numeronym
    if len(num) == 0:
        raise NoNumeronym

    # empty word
    if len(word) == 0:
        raise NoWord

    # number in the word
    if any(x.isnumeric() for x in word):
        raise InvalidNumeronym

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
            print("NOT UNIQUE")
            return False

    return True

data = '''azoisobutyronitrile
o
computer
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

        ('7', 'computer', False),
        ('8', 'computer', True),
        ('9', 'computer', False),

        ('4u3', 'computer', True),
        ('3u4', 'computer', False),
        ('4u4', 'computer', False),
        ('c3u2r', 'computer', True),
        ('1', 'o', True),
    ]
)
def test_check_num2(in1, in2, out):
    assert check_num_list(in1, in2) == out


@pytest.mark.parametrize(
    "in1, in2, exp",
    [
        ('',    'kubernetes', pytest.raises(NoNumeronym)),
        ('k8s', '',           pytest.raises(NoWord)),

    ]
)
def test_check_num2_throws(in1, in2, exp):
    with exp:
        assert check_num_list(in1, in2) is not None


if __name__ == "__main__":
    pass