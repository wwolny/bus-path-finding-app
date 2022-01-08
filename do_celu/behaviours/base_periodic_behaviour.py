#
# do_celu
#
# Copyright 2022 Agenty 007
#

from datetime import datetime
from abc import ABC
from logging import Logger
from typing import Optional
from spade.behaviour import PeriodicBehaviour

from do_celu.config import Config, get_config
from do_celu.context import get_logger


class BasePeriodicBehaviour(PeriodicBehaviour, ABC):
    _logger: Logger
    _config: Config

    def __init__(
        self,
        period: float,
        logger_name: str,
        start_at: Optional[datetime] = None,
    ):
        super().__init__(period, start_at=start_at)
        self._logger = get_logger(logger_name)
        self._config = get_config()
