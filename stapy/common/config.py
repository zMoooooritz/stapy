import logging
import configparser

FILENAME = ".stapy.ini"

class Config:
    """
    This class allows to store and load settings that are relevant for stapy
    Therefore one does not need to pass this arguments each time stapy is used
    """

    def __init__(self, filename=None):
        self.filename = filename
        if filename is None:
            self.filename = FILENAME
        self.config = configparser.ConfigParser()
        self.read()

    def read(self):
        self.config.read(self.filename)

    def save(self):
        with open(self.filename, "w") as configfile:
            self.config.write(configfile)

    def get(self, arg):
        try:
            return self.config["DEFAULT"][arg]
        except KeyError:
            logging.critical("The provided key (" + str(arg) + ") does not exist in the config file")
            return ""

    def set(self, **kwargs):
        for k,v in kwargs.items():
            self.config["DEFAULT"][k] = str(v)


config = Config()

def set_sta_url(sta_url):
    if not isinstance(sta_url, str):
        logging.critical("The provided url (" + str(sta_url) + ") is not valid")
        return
    if not sta_url.endswith("/"):
        sta_url = sta_url + "/"
    config.set(STA_URL = sta_url)
    config.save()

def set_credentials(sta_usr, sta_pwd):
    config.set(STA_USR = sta_usr)
    config.set(STA_PWD = sta_pwd)
    config.save()
