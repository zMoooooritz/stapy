import argparse
import logging

from stapy.sta.post import Post
from stapy.sta.patch import Patch
from stapy.sta.delete import Delete
from stapy.sta.entity import Entity
from stapy.common.log import Log
from stapy.common.config import config, set_api_url
from stapy.cli.cli import main
from stapy.version import __version__


logger = logging.getLogger('root')

class Parser(object):

    args = None

    def __init__(self):
        self.construct_parser()

    def construct_parser(self):
        parser = argparse.ArgumentParser(
            description="Access and modify data that is stored in a server that uses the SensorThings API (v1.1+)",
            prog="stapy", epilog="")
        parser.add_argument("-l", "--log", type=Log.from_string, choices=list(Log), default=Log.WARNING,
                            help="define the log level", metavar="CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET")
        parser.add_argument("-u", "--url", nargs=1, metavar=("URL"),
                            help="set the url of the SensorThings API backend")
        parser.add_argument("-a", "--add", nargs="+", metavar=("Entity", "Parameters"),
                            help="add new entities")
        parser.add_argument("-p", "--patch", nargs="+", metavar=("Entity", "ID"),
                            help="patch existing entities")
        parser.add_argument("-d", "--del", nargs="+", dest="delete", metavar=("Entity", "ID"),
                            help="delete entities by id or path")
        parser.add_argument("-g", "--get", nargs="+", dest="getr", metavar=("Entity", "ID/Path"),
                            help="get the content of entities by id or path")
        parser.add_argument("-i", "--inter", action="store_true",
                            help="start the interactive CLI mode for requests")
        parser.add_argument("-v", "--version", action="version",
                            version="%(prog)s {version}".format(version=__version__))

        self.args = parser.parse_args()

    def get_log_level(self):
        return self.args.log.value

    def parse_args(self):
        if self.args.url:
            set_api_url(self.args.url[0])

        if self.args.add or self.args.patch or self.args.delete or self.args.getr:
            if config.get("API_URL") == "":
                logger.critical("The url has to be set before using the application (see --help)")
                logger.info("ending application")
                return True

        if self.args.add:
            entity = Entity.match(self.args.add[0])
            if entity is None:
                logger.error("The supplied entity (" + self.args.add[0] + ") is not valid")
                logger.error("The valid entities are: " + ", ".join(Entity.list()))
            else:
                ent = Post.get_entity(entity)()
                req_args = ent.req_attributes()
                opt_args = ent.opt_attributes()
                args = {}

                if len(req_args) > len(self.args.add)-1:
                    logger.error("Not enough arguments supplied for the entity " + entity.value)
                    logger.error("The following arguments are mandatory (in this order): " + ", ".join(req_args))
                    logger.error("The following arguments are optional (in this order): " + ", ".join(opt_args))
                else:
                    len_reqs = len(req_args)
                    for index, param in enumerate(req_args):
                        args.update({param: self.args.add[index+1]})
                    for index in range(min(len(self.args.add)-len_reqs-1, len(opt_args))):
                        args.update({opt_args[index]: self.args.add[index+len_reqs+1]})
                    Post.entity(entity, **args)

        if self.args.patch:
            entity = Entity.match(self.args.patch[0])
            if entity is None:
                logger.error("The supplied entity (" + self.args.patch[0] + ") is not valid")
                logger.error("The valid entities are: " + ", ".join(Entity.list()))
            elif len(self.args.patch) == 1:
                logger.error("Missing ID for the " + entity.value + " to patch")
            elif len(self.args.patch) == 2:
                ent = Patch.get_entity(entity)()
                req_args = ent.req_attributes()
                opt_args = ent.opt_attributes()
                logger.error("The entries to edit need to be supplied in the format key=value")
                logger.error("The following arguments are available: " + ", ".join(req_args + opt_args))
            else:
                ent = Patch.get_entity(entity)()
                entity_id = int(self.args.patch[1])
                args = {}

                for arg in self.args.patch[2:]:
                    if not "=" in arg:
                        continue
                    key, value = tuple(arg.split("=", 1))
                    args.update({key: value})
                Patch.entity(entity, entity_id, **args)

        if self.args.delete:
            entity = Entity.match(self.args.delete[0])
            if entity is None:
                logger.error("The supplied entity (" + self.args.delete[0] + ") is not valid")
                logger.error("The valid entities are: " + ", ".join(Entity.list()))
            elif len(self.args.delete) == 1:
                logger.error("Missing ID or path for the deletion")
            else:
                if len(self.args.delete) == 2 and not self.args.delete[1].isdigit():
                    Delete.query(self.args.delete[1])
                else:
                    Delete.entity(entity, self.args.delete[1:])

        if self.args.getr:
            raise NotImplementedError

        if self.args.inter:
            main()
