from enum import Enum

class Request(Enum):
    """
    This class represents all available requests in the SensorThingsAPI (v1.1)
    """
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"

    @staticmethod
    def list():
        """
        :return: a list of all request values
        """
        # return [request.value for request in Request]
        return ["POST", "PATCH", "DELETE"]
