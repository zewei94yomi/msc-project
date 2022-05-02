from enum import Enum


class Status(Enum):
    WAITING = 1
    ACCEPTED = 2
    DELIVERING = 3
    DELIVERED = 4
