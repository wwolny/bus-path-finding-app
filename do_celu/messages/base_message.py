#
# do_celu
#
# Copyright 2022 Agenty 007
#
from abc import ABC, abstractmethod
from typing import Dict, Optional

from spade.message import MessageBase

from do_celu.config import Config, get_config


class BaseMessage(MessageBase, ABC):
    _config: Config

    def __init__(
        self,
        to: Optional[str] = None,
        sender: Optional[str] = None,
        body: Optional[str] = None,
        thread: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            to=to,
            sender=sender,
            body=body,
            thread=thread,
            metadata=metadata,
        )
        self._config = get_config()
        self._set_custom_properties()

    @abstractmethod
    def _set_custom_properties(self) -> None:
        pass
