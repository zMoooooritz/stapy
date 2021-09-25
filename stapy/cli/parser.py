import argparse
import logging

from stapy.sta.post import Post
from stapy.sta.patch import Patch
from stapy.sta.delete import Delete
from stapy.sta.entity import Entity
from stapy.common.log import Log
from stapy.common.config import config, set_api_url
from stapy.cli.cli import CLI
from stapy.version import __version__

logger = logging.getLogger('root')

class Parser(object):

    args = None

    def __init__(self, construct=True):
        if construct:
            self.construct_parser()

    def construct_parser(self):
        parser = argparse.ArgumentParser(
            description="Access and modify data that is stored in a server that uses the SensorThings API (v1.1+)",
            prog="stapy",
            epilog="To get some additional usage information the options add/patch/delete/get can be supplied \
                with the argument 'help'")
        parser.add_argument("-l", "--log", type=Log.from_string, choices=list(Log), default=Log.WARNING,
                            help="define the log level", metavar="CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET")
        parser.add_argument("-u", "--url", nargs=1, metavar=("URL"),
                            help="set the url of the SensorThings API backend")
        parser.add_argument("-a", "--add", nargs="+", metavar=("Entity", "Parameters"),
                            help="add new entities")
        parser.add_argument("-p", "--patch", nargs="+", metavar=("Entity", "ID, Parameters"),
                            help="patch existing entities")
        parser.add_argument("-d", "--del", nargs="+", dest="delete", metavar=("Entity", "ID"),
                            help="delete entities by id or path")
        parser.add_argument("-g", "--get", nargs="+", dest="getr", metavar=("Entity", "ID/Path"),
                            help="get the content of entities by id or path")
        parser.add_argument("-i", "--inter", action="store_true",
                            help="start the interactive CLI mode")
        parser.add_argument("-v", "--version", action="version",
                            version="%(prog)s {version}".format(version=__version__))

        self.args = parser.parse_args()

    def get_log_level(self):
        return self.args.log.value

    def parse_args(self, args=None):
        if args is not None:
            self.args = args

        if self.args.url:
            set_api_url(self.args.url[0])

        if self.args.add or self.args.patch or self.args.delete or self.args.getr or self.args.inter:
            if config.get("API_URL") == "":
                logger.critical("The url has to be set before using the application (see --help)")
                logger.info("ending application")
                return -1

        if self.args.add:
            if self.args.add[0].lower() == "help":
                print("To add a new entity the following syntax needs to be used:")
                print(" First one needs to supply the respective entity")
                print(" The valid entities are: " + ", ".join(Entity.list()))
                print("")
                print("Afterwards each entity needs some mandatory arguments")
                print("Additional optional arguments can be supplied in the format key=value")
                print(" The available arguments can be retrived by replacing the help argument with the respective entity")
                return 1

            entity = Entity.match(self.args.add[0])
            if entity is None:
                logger.error("The supplied entity (" + self.args.add[0] + ") is not valid")
                logger.error("The valid entities are: " + ", ".join(Entity.list()))
                return 3

            ent = Post.get_entity(entity)()
            req_args = ent.req_attributes()
            opt_args = ent.opt_attributes()
            args = {}

            if len(req_args) > len(self.args.add)-1:
                print("Not enough arguments supplied for the entity " + entity.value)
                print("The following arguments are mandatory (in this order): " + ", ".join(req_args))
                print("The following arguments are optional: " + ", ".join(opt_args))
                return 2
            else:
                len_reqs = len(req_args)
                for index, param in enumerate(req_args):
                    args.update({param: self.args.add[index+1]})
                for index in range(min(len(self.args.add)-len_reqs-1, len(opt_args))):
                    arg = self.args.add[index+len_reqs+1]
                    if not "=" in arg:
                        continue
                    key, value = tuple(arg.split("=", 1))
                    args.update({key: value})

                Post.entity(entity, **args)
                return 0

        if self.args.patch:
            if self.args.patch[0].lower() == "help":
                print("To edit an existing entity the following syntax needs to be used:")
                print(" First one needs to supply the respective entity")
                print(" The valid entities are: " + ", ".join(Entity.list()))
                print("")
                print("Afterwards the ID of the entity to modify needs to be specified")
                print("All available arguments are optional and can be supplied in the format key=value")
                print(" The available arguments can be retrived by replacing the help argument with the respective entity and an ID")
                return 1

            entity = Entity.match(self.args.patch[0])
            if entity is None:
                logger.error("The supplied entity (" + self.args.patch[0] + ") is not valid")
                logger.error("The valid entities are: " + ", ".join(Entity.list()))
                return 3
            if len(self.args.patch) == 1:
                print("Missing ID for the " + entity.value + " to patch")
                return 2
            if len(self.args.patch) == 2:
                ent = Patch.get_entity(entity)()
                req_args = ent.req_attributes()
                opt_args = ent.opt_attributes()
                print("The entries to edit need to be supplied in the format key=value")
                print("The following arguments are available: " + ", ".join(req_args + opt_args))
                return 2

            entity_id = int(self.args.patch[1])
            args = {}

            for arg in self.args.patch[2:]:
                if not "=" in arg:
                    continue
                key, value = tuple(arg.split("=", 1))
                args.update({key: value})
            Patch.entity(entity, entity_id, **args)
            return 0

        if self.args.delete:
            if self.args.delete[0].lower() == "help":
                print("To delete an existing entity the following syntax needs to be used:")
                print(" First one needs to supply the respective entity")
                print(" The valid entities are: " + ", ".join(Entity.list()))
                print("")
                print("Afterwards either a list of IDs is specified that are supposed to be deleted")
                print("Or a query path is specified and all entities that satisfy this request will be deleted")
                return 1

            entity = Entity.match(self.args.delete[0])
            if entity is None:
                logger.error("The supplied entity (" + self.args.delete[0] + ") is not valid")
                logger.error("The valid entities are: " + ", ".join(Entity.list()))
                return 3
            if len(self.args.delete) == 1:
                print("Missing ID or path for the deletion")
                return 2

            if len(self.args.delete) == 2 and not self.args.delete[1].isdigit():
                Delete.query(self.args.delete[1])
            else:
                Delete.entity(entity, self.args.delete[1:])
            return 0

        if self.args.getr:
            print("Get request are currently not supported via this interface")
            print("Feel free to implement them yourself and contribute to this project")
            return -1

        if self.args.inter:
            CLI()
            return 0
