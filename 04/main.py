import dataclasses
from typing import List, Iterable, Tuple


def parse_card(card_line) -> Tuple[int, List[int], List[int]]:
    header, numbers = card_line.split(": ")

    card_id = int(header.split(" ")[-1])

    winning_numbers_str, my_numbers_str = numbers.split("|")

    winning_numbers = [int(x) for x in winning_numbers_str.split(" ") if x]
    my_numbers = [int(x) for x in my_numbers_str.split(" ") if x]

    return card_id, winning_numbers, my_numbers


def n_matches(winning_numbers: Iterable[int], my_numbers: List[int]) -> int:
    winning_numbers = set(winning_numbers)
    n_matches = len(winning_numbers.intersection(my_numbers))

    return n_matches

def card_value(winning_numbers: Iterable[int], my_numbers: List[int]) -> int:
    matches = n_matches(winning_numbers, my_numbers)

    if matches == 0:
        return 0

    return 2 ** (matches - 1)


def main():
    total = 0

    with open("input.txt") as f:
        for line in f:
            _, winning_numbers, my_numbers = parse_card(line)
            total += card_value(winning_numbers, my_numbers)

    print(total)


@dataclasses.dataclass
class ScratchCard:
    card_id: int
    winning_numbers: List[int]
    my_numbers: List[int]
    copies: int

    @property
    def n_matches(self) -> int:
        return n_matches(self.winning_numbers, self.my_numbers)

def main_2():
    cards = []

    with open("input.txt") as f:
        for line in f:
            card_id, winning_numbers, my_numbers = parse_card(line)
            cards.append(ScratchCard(card_id, winning_numbers, my_numbers, 1))

    for i, card in enumerate(cards):
        matches = card.n_matches
        for future_card in cards[i + 1: i + 1 + matches]:
            future_card.copies += card.copies

    print(sum(card.copies for card in cards))

if __name__ == '__main__':
    main_2()