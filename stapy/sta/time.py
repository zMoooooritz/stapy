from datetime import date
import dateutil.parser as dparser

class Time(object):

    start_time = None
    end_time = None

    def __init__(self, time=""):
        if not isinstance(time, str):
            raise Exception("Invalid value for time: " + str(time))
        self.start_time = self.parse(time.split("-")[0])
        if "-" in time:
            self.end_time = self.parse(time.split("-")[1])

    def __str__(self):
        if self.start_time is None and self.end_time is None:
            return date.today().isoformat()
        elif self.start_time is not None and self.end_time is None:
            return self.start_time.isoformat()
        elif self.start_time is None and self.end_time is not None:
            return self.end_time.isoformat()
        else:
            if self.start_time == self.end_time:
                return self.start_time.isoformat()
            if self.end_time < self.start_time:
                self.start_time, self.end_time = self.end_time, self.start_time
            return self.start_time.isoformat() + "-" + self.end_time.isoformat()

    def parse(self, date_str):
        try:
            return dparser.parse(date_str, fuzzy=True, dayfirst=True)
        except Exception:
            return None