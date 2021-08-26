#!/usr/bin/env python

from common.log import custom_logger
from common.config import config
from cli.parser import Parser

logger = None

# TODO packages und anordnung fixen, damit alles von allem gefunden wird und die tests klappen
# TODO add documentation (and readme)
# TODO add more tests and make them run properly
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
    return True

run()