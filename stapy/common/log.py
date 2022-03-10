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

def create_logger(level = None):
    """
    Create a basic logger with some special settings
    :param level: the level of log to use
    """
    if level is None:
        level = logging.INFO
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        level=level
    )
