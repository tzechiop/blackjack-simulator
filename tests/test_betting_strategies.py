import copy
import pandas as pd
from parameterized import parameterized
from typing import List
import unittest

from blackjack_simulator.betting_strategies import play_hand
from blackjack_simulator.card import UNIQUE_CARDS
from blackjack_simulator.hand import Hand
from blackjack_simulator.utils import HandAction


TEST_CASES_BOOK_FILENAME = "tests/test_cases_book_with_action.csv"


def set_up_test_cases(test_cases_filename: str,
                      player_card_cols: List,
                      dealer_card_cols: List,
                      expected_action_col: str):
    test_cases_df = pd.read_csv(test_cases_filename)

    test_cases_df['player_hand'] = test_cases_df.apply(
        lambda x: Hand(cards=[copy.deepcopy(UNIQUE_CARDS[x[card_col]])
                              for card_col in player_card_cols],
                       bet=20),
        axis=1)
    test_cases_df['dealer_hand'] = test_cases_df.apply(
        lambda x: Hand(cards=[copy.deepcopy(UNIQUE_CARDS[x[card_col]])
                              for card_col in dealer_card_cols],
                       bet=20),
        axis=1)
    test_cases_df['expected_action'] = test_cases_df[expected_action_col].apply(
        lambda x: getattr(HandAction, x)
    )

    return test_cases_df


test_cases_book = set_up_test_cases(TEST_CASES_BOOK_FILENAME,
                                    ['Player Card 0', 'Player Card 1'],
                                    ['Dealer Card'],
                                    'Action')


class TestPlayHand(unittest.TestCase):
    @parameterized.expand(test_cases_book[['player_hand',
                                           'dealer_hand',
                                           'expected_action']]
                          .values.tolist())
    def test_play_by_book(self,
                          player_hand,
                          dealer_hand,
                          expected_action):
        generated_action = play_hand(player_hand, dealer_hand, 99999)
        self.assertEqual(generated_action,
                         expected_action,
                         ("Generated action was not expected! Generated: "
                          f"{generated_action} / Expected: {expected_action} "
                          f"Player Cards: {player_hand.cards} / Dealer Cards: "
                          f"{dealer_hand.cards}"))
