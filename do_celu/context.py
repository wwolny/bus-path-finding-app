from functools import lru_cache
from logging import Logger, getLogger, basicConfig

from do_celu.config import get_config


@lru_cache()
def get_logger(name: str) -> Logger:
    """
    Args:
        name (str): logger name.
        level (Union[str, int]): logging level. Defaults to `INFO`.
    Returns:
        (logging.Logger) Default application logger.
    """
    basicConfig()
    logger = getLogger(name)
    logger.setLevel(get_config().LOG_LEVEL)
    return logger
