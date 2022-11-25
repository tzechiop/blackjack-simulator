from blackjack_simulator.utils import HandAction, HandStatus


def more_if_possible(more_action, other_action, money, bet):
    if money >= bet or money == -1:
        return more_action
    else:
        return other_action


def play_hand(own: 'Hand',
              dealer: 'Hand',
              money: float):
    if len(own.cards) == 2 and own.cards[0].name == own.cards[1].name:
        if own.cards[0].value <= 3:
            if dealer.value <= 7:
                return more_if_possible(HandAction.SPLIT,
                                        HandAction.HIT,
                                        money,
                                        own.bet)
            else:
                return HandAction.HIT
        elif own.cards[0].value == 4:
            if dealer.value == 5 or dealer.value == 6:
                return more_if_possible(HandAction.SPLIT,
                                        HandAction.HIT,
                                        money,
                                        own.bet)
            else:
                return HandAction.HIT
        elif own.cards[0].value == 5:
            if dealer.value <= 9:
                return more_if_possible(HandAction.DOUBLE,
                                        HandAction.HIT,
                                        money,
                                        own.bet)
            else:
                return HandAction.HIT
        elif own.cards[0].value == 6:
            if dealer.value <= 6:
                return more_if_possible(HandAction.SPLIT,
                                        HandAction.HIT,
                                        money,
                                        own.bet)
            else:
                return HandAction.HIT
        elif own.cards[0].value == 7:
            if dealer.value <= 7:
                return more_if_possible(HandAction.SPLIT,
                                        HandAction.HIT,
                                        money,
                                        own.bet)
            else:
                return HandAction.HIT
        elif own.cards[0].value == 8 or own.cards[0].value == 11:
            return more_if_possible(HandAction.SPLIT,
                                    HandAction.HIT,
                                    money,
                                    own.bet)
        elif own.cards[0].value == 9:
            if dealer.value == 7 or dealer.value >= 10:
                return HandAction.STAND
            else:
                return more_if_possible(HandAction.SPLIT,
                                        HandAction.STAND,
                                        money,
                                        own.bet)
        else:
            return HandAction.STAND
    elif own.hand_status == HandStatus.HARD:
        if own.value <= 8:
            return HandAction.HIT
        elif own.value == 9:
            if 3 <= dealer.value <= 6:
                return more_if_possible(HandAction.DOUBLE,
                                        HandAction.HIT,
                                        money,
                                        own.bet)
            else:
                return HandAction.HIT
        elif own.value == 10:
            if dealer.value <= 9:
                return more_if_possible(HandAction.DOUBLE,
                                        HandAction.HIT,
                                        money,
                                        own.bet)
            else:
                return HandAction.HIT
        elif own.value == 11:
            return more_if_possible(HandAction.DOUBLE,
                                    HandAction.HIT,
                                    money,
                                    own.bet)
        elif own.value == 12:
            if 4 <= dealer.value <= 6:
                return HandAction.STAND
            else:
                return HandAction.HIT
        elif own.value <= 16:
            if dealer.value <= 6:
                return HandAction.STAND
            else:
                return HandAction.HIT
        else:
            return HandAction.STAND
    elif own.hand_status == HandStatus.SOFT:
        if own.value <= 14:
            if 5 <= dealer.value <= 6:
                return more_if_possible(HandAction.DOUBLE,
                                        HandAction.HIT,
                                        money,
                                        own.bet)
            else:
                return HandAction.HIT
        elif own.value <= 16:
            if 4 <= dealer.value <= 6:
                return more_if_possible(HandAction.DOUBLE,
                                        HandAction.HIT,
                                        money,
                                        own.bet)
            else:
                return HandAction.HIT
        elif own.value == 17:
            if 3 <= dealer.value <= 6:
                return more_if_possible(HandAction.DOUBLE,
                                        HandAction.HIT,
                                        money,
                                        own.bet)
            else:
                return HandAction.HIT
        elif own.value == 18:
            if dealer.value <= 6:
                return more_if_possible(HandAction.DOUBLE,
                                        HandAction.HIT,
                                        money,
                                        own.bet)
            elif dealer.value <= 8:
                return HandAction.STAND
            else:
                return HandAction.HIT
        elif own.value == 19:
            if dealer.value == 6:
                return more_if_possible(HandAction.DOUBLE,
                                        HandAction.STAND,
                                        money,
                                        own.bet)
            else:
                return HandAction.STAND
        else:
            return HandAction.STAND
    else:
        raise ValueError(f"Hand status {own.hand_status} not detected!")
