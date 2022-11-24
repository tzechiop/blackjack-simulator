import copy
from dataclasses import dataclass
import numpy as np
from typing import List


@dataclass
class Card:
    name: str
    value: int
    hidden: bool = None
    is_soft: bool = None

    def __repr__(self):
        return self.name


class Shoe:
    def __init__(self,
                 cards: List[Card],
                 cut_loc: int = None):
        self.cards = cards
        self.cut_loc = cut_loc

    @classmethod
    def create_shoe(cls,
                    num_decks: int = 6,
                    num_suites: int = 4,
                    shuffle: bool = True,
                    cut: bool = True,
                    unique_cards: List[Card] = None,
                    seed=None):
        if unique_cards is None:
            unique_cards = UNIQUE_CARDS

        np.random.seed(seed)
        cards = []
        for _ in range(num_decks):
            for _ in range(num_suites):
                cards.extend([copy.deepcopy(card) for card in unique_cards])

        if shuffle:
            np.random.shuffle(cards)

        if cut:
            cut_perc = bound(0, 0.5, np.random.normal(0.25, 0.05))
            cut_loc = round(cut_perc * len(cards))
            cards = cards[-cut_loc:] + cards[:-cut_loc]
        else:
            cut_loc = 1

        return cls(cards, cut_loc)

    def __len__(self):
        return len(self.cards)


def bound(low, high, value):
    return max(low, min(high, value))


UNIQUE_CARDS = [
    Card('Two', 2),
    Card('Three', 3),
    Card('Four', 4),
    Card('Five', 5),
    Card('Six', 6),
    Card('Seven', 7),
    Card('Eight', 8),
    Card('Nine', 9),
    Card('Ten', 10),
    Card('Jack', 10),
    Card('Queen', 10),
    Card('King', 10),
    Card('Ace', 11)
]
