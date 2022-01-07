#
# do_celu
#
# Copyright 2022 Agenty 007
#
from spade.message import Message
from spade.template import Template

from do_celu.utils.performatives import Performatives
from do_celu.messages.base_message import BaseMessage


class _DriverDataMessageBase(BaseMessage):

    def _set_custom_metadata(self) -> None:
        self.set_metadata("performative", Performatives.REQUEST.value)
        self.set_metadata("ontology", self._config.ONTOLOGY)
        self.set_metadata("language", "JSON")
        self.set_metadata('behaviour', 'driver_data')


class DriverDataTemplate(_DriverDataMessageBase, Template):
    pass


class DriverDataMessage(_DriverDataMessageBase, Message):
    pass


class _PathChangeMessageBase(BaseMessage):

    def _set_custom_metadata(self) -> None:
        self.set_metadata("performative", Performatives.INFORM.value)
        self.set_metadata("ontology", self._config.ONTOLOGY)
        self.set_metadata("language", "JSON")
        self.set_metadata('behaviour', 'path_change')


class PathChangeTemplate(_PathChangeMessageBase, Template):
    pass


class PathChangeMessage(_PathChangeMessageBase, Message):
    pass
