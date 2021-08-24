#!/usr/bin/env python

import argparse
import requests
from inspect import signature

from sta.entity import Entity
from sta.post import Post
from sta.query import Query, Expand
from sta.json import JSONExtract
from common.log import Log, custom_logger
from common.config import config
import cli

logger = None

# TODO consistent naming and argument order in post.py
# TODO add documentation (and readme)
# TODO add more tests and make them run properly
# TODO allow for patch / update
# TODO improve CLI Dialogs

def run():

    parser = argparse.ArgumentParser(
        description="Access and modify data that is stored in a server that uses the SensorThings API (v1.1+)",
        prog="STApy", epilog="")
    parser.add_argument("-l", "--log", type=Log.from_string, choices=list(Log), default=Log.INFO,
                        help="define the log level", metavar="CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET")
    parser.add_argument("-u", "--url-set", dest="urlset", nargs=1, metavar=("URL"),
                        help="set the url of the SensorThings API backend")
    parser.add_argument("-ug", "--url-get", dest="urlget", action="store_true",
                        help="get the url of the SensorThings API backend")
    parser.add_argument("-a", "--add", nargs="+", metavar=("Entity", "Parameters"),
                        help="add new entities")
    parser.add_argument("-d", "--del", nargs="+", dest="delete", metavar=("Entity", "ID"),
                        help="delete entities by id or path")
    parser.add_argument("-g", "--get", nargs="+", dest="getr", metavar=("Entity", "ID/Path"),
                        help="get the content of entities by id or path")
    parser.add_argument("-i", "--inter", action="store_true",
                        help="start the interactive CLI mode for requests")

    args = parser.parse_args()

    global logger
    logger = custom_logger('root', args.log.value)
    logger.info("starting application")

    if args.urlset:
        url = args.urlset
        if isinstance(args.urlset, list):
            url = args.urlset[0]
        url = str(url)
        if not url.endswith("/"):
            url = url + "/"
        config.set(API_URL = url)
    if args.urlget:
        print("The currently set API_URL is: " + str(config.get("API_URL")))

    if (args.add or args.delete or args.getr) and config.get("API_URL") == "":
        logger.critical("The url has to be set before using the application (see --help)")
        logger.info("ending application")
        return True

    if args.add:
        func = Post.get_entity_method(args.add[0])
        if func == None:
            logger.error("The supplied entity (" + args.add[0] + ") is not valid")
            logger.error("The valid entities are: " + ", ".join(Entity.list()))
        else:
            req_args = []
            for param in signature(func).parameters.values():
                if param.default is param.empty:
                    req_args.append(param.name)

            if len(req_args) > len(args.add)-1:
                logger.error("Not enough arguments supplied for the entity " + Entity.get(args.add[0]).value)
                logger.error("The following arguments are mandatory (in this order): " + ", ".join(req_args))
            else:
                Post.new_entity(args.add[0], *args.add[1:])

    if args.delete:
        entity = Entity.get(args.delete[0])
        if entity == None:
            logger.error("The supplied entity (" + args.delete[0] + ") is not valid")
            logger.error("The valid entities are: " + ", ".join(Entity.list()))
        else:
            for e_id in args.delete[1:]:
                if e_id.isdigit():
                    requests.delete(Query(entity.value).entity_id(int(e_id)).get_query())
                else:
                    logger.warning(str(e_id) + " is not a valid " + entity.value + "-ID")

    if args.getr:
        # path = Query(Entity.Locations.value).get_query()
        # print(JSONExtract(path).select("name").get_data_sets())
        pass

    if args.inter:
        cli.request()

    config.save()

    logger.info("ending application")
    return True

run()
