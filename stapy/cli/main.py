from stapy.common.log import custom_logger
from stapy.common.config import config
from stapy.cli.parser import Parser

def main():
    """
    This is the main entry point of the stapy application in case it is not used as library
    """

    parser = Parser()

    logger = custom_logger("root", parser.get_log_level())

    logger.info("starting application")

    parser.parse_args()

    config.save()

    logger.info("ending application")

if __name__ == "__main__":
    main()