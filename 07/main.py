from collections import Counter
import dataclasses
from enum import IntEnum

from typing import Dict, List, Tuple


class HandType(IntEnum):
    FiveOfAKind = 7
    FourOfAKind = 6
    FullHouse = 5
    ThreeOfAKind = 4
    TwoPair = 3
    OnePair = 2
    HighCard = 1

card_strength_order = "AKQT98765432J"
card_strength_mapping = {card: value for value, card in enumerate(card_strength_order[::-1])}

card_count_mapping: Dict[Tuple, HandType] = {
    (5,): HandType.FiveOfAKind,
    (4, 1): HandType.FourOfAKind,
    (3, 2): HandType.FullHouse,
    (3, 1, 1): HandType.ThreeOfAKind,
    (2, 2, 1): HandType.TwoPair,
    (2, 1, 1, 1): HandType.OnePair,
    (1, 1, 1, 1, 1): HandType.HighCard
}

@dataclasses.dataclass
class Hand:
    cards: str
    bid: int

    def __repr__(self):
        return f"{self.cards} ({self.bid})"

    @property
    def hand_type(self) -> HandType:
        card_counter = Counter(self.cards)
        if 'J' in card_counter:
            j_val = card_counter['J']
            del card_counter['J']

            if card_counter:
                max_key = max(card_counter.keys(), key=lambda x: card_counter[x])
                card_counter[max_key] += j_val
            else:
                card_counter["K"] = j_val

        values = tuple(sorted(card_counter.values(), reverse=True))


        if values not in card_count_mapping:
            raise ValueError(f"values not in card_count_mapping. Values: {values}, cards: {self.cards}")

        return card_count_mapping[values]

    @property
    def card_values(self) -> List[int]:
        return [card_strength_mapping[a] for a in self.cards]

    def __lt__(self, other: "Hand"):
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type

        return self.card_values < other.card_values


def parse_hands():
    with open("input.txt") as f:
        lines = f.readlines()

    hands: List[Hand] = []

    for line in lines:
        cards, bid_str = line.split()
        bid = int(bid_str)

        hand = Hand(cards, bid)
        hands.append(hand)

    return hands

def main():
    hands = parse_hands()

    hands = sorted(hands)
    total_winnings = sum(hand.bid * rank for rank, hand in enumerate(hands, start=1))
    print(total_winnings)


if __name__ == "__main__":
    main()