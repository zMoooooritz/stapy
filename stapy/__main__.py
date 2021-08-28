from stapy.common.log import custom_logger, Log
from stapy.common.config import config

logger = None
global logger
logger = custom_logger('root', Log.from_string(config.get("LOG_LEVEL")))