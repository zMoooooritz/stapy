import logging
import requests
import configparser

from stapy.common.log import DEFAULT_LOG_LEVEL

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
            return None

    def set(self, **kwargs):
        for k,v in kwargs.items():
            self.config["DEFAULT"][k] = str(v)

    def remove(self, arg):
        try:
            return self.config.remove_option("DEFAULT", arg)
        except NoSectionError:
            return False

    def load_log_lvl(self):
        try: 
            log_lvl = int(self.get("LOG_LVL"))
        except (ValueError, TypeError):
            log_lvl = DEFAULT_LOG_LEVEL
        return log_lvl

    def load_sta_url(self):
        sta_url = self.get("STA_URL")
        if sta_url is None:
            logging.critical("The key (STA_URL) does not exist in the config file set the url first")
        return sta_url

    def load_authentication(self):
        sta_usr = self.get("STA_USR")
        sta_pwd = self.get("STA_PWD")
        if sta_usr is None or sta_pwd is None:
            logging.debug("Sending the request without credentials")
            return None
        else:
            logging.debug("Sending the request without credentials")
            return requests.auth.HTTPBasicAuth(sta_usr, sta_pwd)


config = Config()

def set_log_level(log_lvl):
    config.set(LOG_LVL = log_lvl)
    config.save()

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
