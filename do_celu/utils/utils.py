#
# do_celu
#
# Copyright 2022 Agenty 007
#

from spade.message import Message

from do_celu.config import Config


def create_message(
    config_file: Config, send_to: str, performative: str, msg_body: str
) -> Message:
    msg = Message(to=send_to)
    msg.set_metadata("performative", performative)
    msg.set_metadata("ontology", config_file.ONTOLOGY)
    msg.set_metadata("langauge", "JSON")
    msg.body = msg_body
    return msg
