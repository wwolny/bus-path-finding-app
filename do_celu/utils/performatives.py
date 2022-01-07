from enum import Enum


class Performatives(Enum, str):
    INFORM = 'inform'
    REQUEST = 'request'
    PROPOSE = 'propose'
