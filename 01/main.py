from typing import Optional

WORD_NUMBERS = [
    'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'
]

VALID_NUMBERS = {
    **{str(i): i for i in range(10)},
    **{word: i for i, word in enumerate(WORD_NUMBERS)}
}

def get_first_digit(s: str) -> Optional[int]:
    min_loc = len(s)
    min_val = None

    for word, val in VALID_NUMBERS.items():
        loc = s.find(word)

        if loc != -1 and loc < min_loc:
            min_loc = loc
            min_val = val

    return min_val

def get_last_digit(s: str) -> Optional[int]:
    max_loc = -1
    max_val = None

    for word, val in VALID_NUMBERS.items():
        loc = s.rfind(word)

        if loc != -1 and loc > max_loc:
            max_loc = loc
            max_val = val

    return max_val

def get_number(s: str) -> int:
    first_digit = get_first_digit(s)
    last_digit = get_last_digit(s)

    assert first_digit is not None and last_digit is not None

    return first_digit * 10 + last_digit

def main():
    input_file = open('input.txt', 'r')

    total = sum(get_number(line) for line in input_file)

    print(total)



if __name__ == '__main__':
    main()