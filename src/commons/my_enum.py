from enum import Enum


class OrderStatus(Enum):
    WAITING = 1
    ACCEPTED = 2
    DELIVERING = 3
    COMPLETE = 4


class DroneStatus(Enum):
    WAITING = 1
    COLLECTING = 2
    DELIVERING = 3
    RETURNING = 4
