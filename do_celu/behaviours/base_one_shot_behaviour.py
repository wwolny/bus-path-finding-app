#
# do_celu
#
# Copyright 2022 Agenty 007
#

from abc import ABC
from logging import Logger

from spade.behaviour import OneShotBehaviour

from do_celu.config import Config, get_config
from do_celu.context import get_logger


class BaseOneShotBehaviour(OneShotBehaviour, ABC):
    _logger: Logger
    _config: Config

    def __init__(self, logger_name: str):
        super().__init__()
        self._config = get_config()
        self._logger = get_logger(logger_name)
