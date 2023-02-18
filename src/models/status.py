from enum import Enum


class Status(Enum):
    """ Represent the status for the component """
    
    OFF = "OFF"
    RUNNING = "RUNNING"
    ERROR = "ERROR"