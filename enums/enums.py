from enum import Enum


class CommandEnum(Enum):
    Connect = 1
    Disconnect = 2
    Stop = 3
    Subscribe = 4
    Unsubscribe = 5
    Play = 6


class ConfirmationEnum(Enum):
    Yes = 1
    No = 2
