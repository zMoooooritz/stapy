from STAPy.common.log import custom_logger
from STAPy.common.config import config
from STAPy.cli.parser import Parser

logger = None

# TODO make the correct logger run in non app.py mode as well -> loglevel in config file
# TODO add documentation (and readme)
# TODO add more tests
# TODO improve CLI Dialogs
# TODO allow for patch / update

def run():
    parser = Parser()

    global logger
    logger = custom_logger('root', parser.get_log_level())
    logger.info("starting application")

    parser.parse_args()

    config.save()

    logger.info("ending application")