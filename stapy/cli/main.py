import logging

from stapy.common.log import create_logger
from stapy.common.config import config
from stapy.cli.parser import Parser

def main():
    """
    This is the main entry point of the stapy application in case it is not used as library
    """

    parser = Parser()

    create_logger(parser.get_log_level())

    logging.info("starting application")

    parser.parse_args()

    config.save()

    logging.info("ending application")

if __name__ == "__main__":
    main()