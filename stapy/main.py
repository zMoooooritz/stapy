from stapy.common.log import custom_logger
from stapy.common.config import config
from stapy.cli.parser import Parser
import logging

# TODO make the correct logger run in non app.py mode as well -> loglevel in config file
# TODO add documentation (and readme)
# TODO add more tests
# TODO improve CLI Dialogs
# TODO allow for patch / update

logger = logging.getLogger('root')

def run():
    parser = Parser()

    logger.info("starting application")

    parser.parse_args()

    config.save()

    logger.info("ending application")