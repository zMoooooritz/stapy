from stapy.sta.entity import Entity
from stapy.sta.post import Post
from stapy.sta.patch import Patch
from stapy.sta.delete import Delete
from stapy.sta.query import Query
from stapy.common.config import config, set_log_level, set_sta_url, set_credentials
from stapy.common.log import setup_logger

__all__ = (
    ["Entity"] +
    ["Post"] +
    ["Patch"] +
    ["Delete"] +
    ["Query"] +
    ["set_log_level"] +
    ["set_sta_url"] +
    ["set_credentials"]
)

setup_logger(config.load_log_lvl())
