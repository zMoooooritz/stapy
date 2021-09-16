import logging
from enum import Enum

class Log(Enum):
    """
    An Enum that represents all available log levels
    """
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    @staticmethod
    def from_string(log):
        """
        Convert a string into a Log key
        :param log: the string to convert
        :return: the resulting key
        """
        try:
            return Log[log]
        except KeyError:
            return Log.NOTSET


def custom_logger(name, level):
    """
    Create a basic logger with some special settings
    :param name: the name of the logger
    :param level: the level of log to use
    :return: the resulting logger
    """
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
