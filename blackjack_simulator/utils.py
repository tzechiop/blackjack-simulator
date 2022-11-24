from enum import Enum


class HandAction(Enum):
    STAND = 1
    HIT = 2
    DOUBLE = 3
    SPLIT = 4


class HandStatus(Enum):
    BUST = 0
    STAND = 1
    HARD = 2
    SOFT = 3
    DOUBLE = 4
    SPLIT = 5
