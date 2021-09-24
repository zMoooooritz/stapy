import logging
import configparser

logger = logging.getLogger('root')

FILENAME = "config.ini"

class Config:

    def __init__(self, filename=None):
        self.filename = filename
        if filename is None:
            self.filename = FILENAME
        self.config = configparser.ConfigParser()
        self.read()

    def read(self):
        self.config.read(self.filename)

    def save(self):
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)

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
