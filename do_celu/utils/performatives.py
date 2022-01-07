from enum import Enum


class Performatives(str, Enum):
    INFORM = 'inform'
    REQUEST = 'request'
    PROPOSE = 'propose'
