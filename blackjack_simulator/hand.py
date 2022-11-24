from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional

from blackjack_simulator.betting_strategies import play_hand
from blackjack_simulator.card import Card
from blackjack_simulator.utils import HandAction, HandStatus


@dataclass
class Hand:
    cards: List[Optional[Card, Hand]] = None
    bet: float = None
    hand_status: HandStatus = HandStatus.HARD
    is_dealer: bool = None
    is_double: bool = None

    def __post_init__(self):
        if self.cards is None:
            self.cards = []

        if self.cards:
            self.calculate_value()

    @property
    def value(self):
        if isinstance(self.cards[0], Card):
            return self.calculate_value()

    @property
    def is_blackjack(self):
        not_split = all([isinstance(card, Card) for card in self.cards])
        return (not_split and len(self.cards) == 2 and
                ((self.cards[0].name == 'Ace' and self.cards[1].value == 10) or
                 (self.cards[1].name == 'Ace' and self.cards[0].value == 10)))

    def calculate_value(self):
        aces = []
        value = 0
        value += sum([card.value for card in self.cards if card.name != 'Ace' and not card.hidden])

        # handle the aces
        is_soft = False
        for ace in [card for card in self.cards if card.name == 'Ace' and not card.hidden]:
            if value + 11 > 21:
                value += 1
            else:
                value += 11
                is_soft = True

        if is_soft:
            self.hand_status = HandStatus.SOFT

        if value > 21:
            self.hand_status = HandStatus.BUST

        return value

    def play(self,
             table: Table,
             money: float):
        continue_play = True
        while continue_play and self.hand_status != HandStatus.BUST:
            action = play_hand(self, table.dealer.hand, money, self.bet)
            continue_play, table, money = self.resolve_play(action, table, money)

        return table, money

    def dealer_play(self,
                    table):
        for card in self.cards:
            card.hidden = False

        while (self.hand_status != HandStatus.BUST or (self.hand_status == HandStatus.SOFT and self.value <= 17) \
               or (self.hand_status == HandStatus.HARD and self.value < 17)):
            __, table, __ = self.resolve_play(HandAction.HIT, table)
        return table

    def resolve_play(self,
                     action: HandAction,
                     table: Table,
                     money: float = None):
        if action == HandAction.STAND:
            self.hand_status = HandStatus.STAND

            return False, table, money
        elif action == HandAction.HIT:
            table.deal_one_card(self)

            return True, table, money
        elif action == HandAction.DOUBLE:
            money -= self.bet
            self.hand_status = HandStatus.DOUBLE
            table.deal_one_card(self)

            return False, table, money
        elif action == HandAction.SPLIT:
            self.cards = [Hand(cards=[self.cards.pop()], bet=self.bet),
                          Hand(cards=[self.cards.pop()], bet=self.bet)]
            money -= self.bet
            self.bet = 0
            self.hand_status = HandStatus.SPLIT
            for split_hand in self.cards:
                table.deal_one_card(split_hand)
                table, money = split_hand.play(table,
                                               money)
            return False, table, money
        else:
            raise ValueError(f"HandAction {action} not recognized!")

    def resolve_bet(self,
                    dealer_hand):
        result = 0
        if self.hand_status == HandStatus.SPLIT:
            for split_hand in self.cards:
                result += split_hand.resolve_bet(dealer_hand)

                print(f"result: {result} / {split_hand.cards} / {dealer_hand.cards}")
        elif self.hand_status != HandStatus.BUST and ~dealer_hand.is_blackjack:
            if self.value == dealer_hand.value:
                result += self.bet
            elif dealer_hand.hand_status == HandStatus.BUST or self.value > dealer_hand.value:
                result += self.bet * 2
            print(f"result: {result} / {self.cards} / {dealer_hand.cards}")

        return result

