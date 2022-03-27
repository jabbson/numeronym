# Write me a function that can determine if a word is a numeronym.
import pytest

def check_num(num: str, word: str) -> bool:
    num = num.lower()
    word = word.lower()

    if len(num) == 0:
        return False

    # numeronym is too short
    if len(num) == 1:
        return False

    if num[0].isnumeric() or num[-1].isnumeric():
        return False

    # empty word
    if len(word) == 0:
        return False

    # two letter words
    if len(num) == 2 and num == word:
        return True

    if num[0] != word[0] or num[-1] != word[-1]:
        return False

    try:
        n = int(num[1:-1])
    except:
        return False

    if len(word[1:-1]) != n:
        return False

    return True

@pytest.mark.parametrize(
    "in1, in2, out",
    [
        ('k8s',  'kubernetes',              True),
        ('K8s',  'kubernetes',              True),
        ('i18n', 'internationalization',    True),
        ('k9s',  'kubernetes',              False),
        ('k8s',  'test',                    False),
        ('at',   'at',                      True),
        ('at',   'ta',                      False),
        ('a0t',  'at',                      True),
        ('',     'test',                    False),
        ('t',    'test',                    False),
        ('k8s',  '',                        False),
    ]
)
def test_check_num(in1, in2, out):
    assert check_num(in1, in2) == out

if __name__ == "__main__":
    # print(check_num('a0t', 'at'))
    pass
