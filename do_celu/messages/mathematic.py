#
# do_celu
#
# Copyright 2022 Agenty 007
#
from dataclasses import dataclass
from typing import List, Tuple
from spade.message import Message
from spade.template import Template

from do_celu.utils.performatives import Performatives
from do_celu.messages.base_message import BaseMessage


class _RequestBestPathsBase(BaseMessage):

    def _set_custom_properties(self) -> None:
        self.set_metadata("performative", Performatives.REQUEST.value)
        self.set_metadata("ontology", self._config.ONTOLOGY)
        self.set_metadata("language", "JSON")
        self.set_metadata('behaviour', 'request_best_paths')


class RequestBestPathsTemplate(_RequestBestPathsBase, Template):
    pass


class RequestBestPathsMessage(_RequestBestPathsBase, Message):
    pass


@dataclass(frozen=True)
class RequestBestPathsBody():
    """
    Args:
        bus_routes (List[List[int]]): List of routes of busses.
        new_ride (Tuple[int, int]): Needed ride from bus stop to bus stop.
    """
    bus_routes: List[List[int]]
    new_rides: List[Tuple[int, int]]
