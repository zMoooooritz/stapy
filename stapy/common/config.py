import logging
import sys
import configparser

logger = logging.getLogger('root')

class Config:

    FILENAME = "config.ini"

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.read()

    def read(self):
        try:
            self.config.read(self.FILENAME)
        except Exception:
            logger.error("Config file does not exist creating empty config file")
            self.set(API_URL = "")
            self.save()

    def save(self):
        try:
            with open(self.FILENAME, 'w') as configfile:
                self.config.write(configfile)
        except configparser.Error:
            logger.critical("Writing the config file did fail")
            logger.info("ending application")
            sys.exit()

    def get(self, arg):
        try:
            return self.config["DEFAULT"][arg]
        except KeyError:
            logger.critical("The provided key (" + str(arg) + ") does not exist in the config file")
            return ""

    def set(self, **kwargs):
        for k,v in kwargs.items():
            self.config["DEFAULT"][k] = str(v)


config = Config()

def set_api_url(api_url):
    if not isinstance(api_url, str):
        logger.critical("The provided url (" + str(api_url) + ") is not valid")
        return
    if not api_url.endswith("/"):
        api_url = api_url + "/"
    config.set(API_URL = api_url)
    config.save()
