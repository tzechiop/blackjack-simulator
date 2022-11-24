from __future__ import annotations
from dataclasses import dataclass
from typing import List

from blackjack_simulator.card import Shoe
from blackjack_simulator.hand import Hand
from blackjack_simulator.utils import HandStatus


@dataclass
class Seat:
    money: int
    track_money: bool = True
    is_dealer: bool = False
    hand: Hand = None
    in_play: bool = True

    @classmethod
    def create_pc(cls, money):
        return cls(money, track_money=True, is_dealer=False)

    @classmethod
    def create_npc(cls):
        return cls(money=-1, track_money=False, is_dealer=False)

    @classmethod
    def create_dealer(cls):
        return cls(money=-1, track_money=False, is_dealer=True)

    def make_min_bet(self,
                     min_bet: int):
        if not self.track_money or self.money >= min_bet:
            if self.track_money:
                self.money -= min_bet
            self.hand = Hand(bet=min_bet)
            self.in_play = True
            return
        else:
            self.in_play = False

    def play_hand(self,
                  table: Table):
        table, money = self.hand.play(table,
                                      self.money)
        self.money = money
        return table


@dataclass
class Table:
    seats: List[Seat] = None
    dealer: Seat = None
    shoe: Shoe = None
    min_bet: int = 20

    @classmethod
    def create_table(cls, seat_money_vals: list, shoe_kwargs: dict = None):
        if shoe_kwargs is None:
            shoe_kwargs = {}

        seats = []
        for seat_money in seat_money_vals:
            if seat_money == -1:
                seats.append(Seat.create_npc())
            else:
                seats.append(Seat.create_pc(seat_money))
        return cls(seats=seats,
                   dealer=Seat.create_dealer(),
                   shoe=Shoe.create_shoe(**shoe_kwargs))

    def deal_one_card(self, hand: Hand, make_hidden: bool = False):
        card_to_deal = self.shoe.cards.pop()
        if make_hidden:
            card_to_deal.hidden = True

        hand.cards.append(card_to_deal)
        hand.calculate_value()

        return hand.hand_status != HandStatus.BUST

    def deal_one_card_to_all(self):
        for seat in self.seats:
            if seat.in_play:
                self.deal_one_card(seat.hand)

    def gather_bets(self):
        for seat in self.seats:
            seat.make_min_bet(self.min_bet)

        self.dealer.hand = Hand(is_dealer=True)

    def deal(self):
        if len(self.shoe) > self.shoe.cut_loc:
            # first card
            self.deal_one_card_to_all()
            self.deal_one_card(self.dealer.hand, make_hidden=False)

            # second card
            self.deal_one_card_to_all()
            self.deal_one_card(self.dealer.hand, make_hidden=True)

            return True
        else:
            return False

    def resolve_insurance(self):
        pass

    def play_all_hands(self):
        for seat in self.seats:
            if seat.in_play:
                self = seat.play_hand(self)
        self = self.dealer.hand.dealer_play(self)

    def resolve_bets(self):
        for seat in self.seats:
            result = seat.hand.resolve_bet(self.dealer.hand)
            seat.money += result

    def clean_table(self):
        for seat in self.seats:
            seat.hand = None
        self.dealer.hand = None
