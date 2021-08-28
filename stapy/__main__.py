from stapy.common.log import custom_logger, Log
from stapy.common.config import config
from stapy.cli.parser import Parser
import logging

parser = Parser()

logger = custom_logger('root', Log.from_string(config.get("LOG_LEVEL")))
# logger = logging.getLogger('root')

logger.info("starting application")

parser.parse_args()

config.save()

logger.info("ending application")