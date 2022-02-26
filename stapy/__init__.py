from stapy.sta.entity import Entity
from stapy.sta.post import Post
from stapy.sta.patch import Patch
from stapy.sta.delete import Delete
from stapy.sta.query import Query
from stapy.common.config import set_sta_url, set_credentials

__all__ = (
    ["Entity"] +
    ["Post"] +
    ["Patch"] +
    ["Delete"] +
    ["Query"] +
    ["set_sta_url"] +
    ["set_credentials"]
)