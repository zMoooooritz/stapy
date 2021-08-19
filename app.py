#!/usr/bin/env python

from sta.entity import Entity
from sta.post import Post
from sta.query import Query, Expand
from common.log import Log, custom_logger

import argparse

logger = None

def run():

    parser = argparse.ArgumentParser(
        description="Access and modify data that is stored in a server that uses the SensorThings API (v1.1+)",
        prog="STApy", epilog="")
    parser.add_argument("-d", "--del", "--delete", nargs="+", dest="delete", metavar=("Entity", "ID/Path"),
                        help="delete entities by id or path")
    parser.add_argument("-l", "--log", type=Log.from_string, choices=list(Log), default=Log.INFO,
                        help="define the log level", metavar="CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET")

    args = parser.parse_args()

    global logger
    logger = custom_logger('root', args.log.value)
    logger.info("starting application")

    # Add requests here

    logger.info("ending application")
    return True

run()
