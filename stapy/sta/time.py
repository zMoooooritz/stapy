from datetime import date
import dateutil.parser as dparser

class Time(object):
    """
    This class represents a singular time or a time interval
    """

    start_time = None
    end_time = None

    def __init__(self, time=""):
        """
        Construct the time object as time or interval depending on incoming time parameter
        :param time: string representation of the time / time interval
        """
        if not isinstance(time, str):
            raise Exception("Invalid value for time: " + str(time))
        self.start_time = self.parse(time.split("-")[0])
        if "-" in time:
            self.end_time = self.parse(time.split("-")[1])

    def __str__(self):
        """
        Return the string representing this time object
        """
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
        """
        This method gets a string representing a date and converts it to a python datetime
        :param date_str: string representation of the date
        :return: the datetime or None if the provided date_str cant be converted
        """
        try:
            return dparser.parse(date_str, fuzzy=True, dayfirst=True)
        except Exception:
            return None