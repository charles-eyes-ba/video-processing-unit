from enum import Enum


class DetectorStatus(Enum):
    OFF = "OFF"
    RUNNING = "RUNNING"
    ERROR = "ERROR"