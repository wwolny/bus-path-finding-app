from enum import Enum


class Performatives(Enum, str):
    INFORM = 'inform'
    REQUEST = 'request'
    PROPOSE = 'propose'
    CALL_FOR_PROPOSAL = 'call_for_proposal'
    ACCEPT_PROPOSAL = 'accept_proposal'
