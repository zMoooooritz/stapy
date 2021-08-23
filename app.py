#!/usr/bin/env python

from sta.entity import Entity
from sta.post import Post
from sta.query import Query, Expand
from common.log import Log, custom_logger
from common.config import Config

import argparse

logger = None

# TODO implement add / del / get in a basic way
# TODO add documentation (and readme)
# TODO add more tests and make them run properly
# TODO allow for patch / update
# TODO add CLI - Dialogs for add / del / get

def run():

    config = Config()

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
    parser.add_argument("-d", "--del", nargs="+", dest="delete", metavar=("Entity", "ID/Path"),
                        help="delete entities by id or path")
    parser.add_argument("-g", "--get", nargs="+", dest="getr", metavar=("Entity", "ID/Path"),
                        help="get the content of entities by id or path")

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



    # Add requests here
    # Post().new_location("Test-Location", "Test-Location-Description", "Lul", [0])

    config.save()

    logger.info("ending application")
    return True

run()
