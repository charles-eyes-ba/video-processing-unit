from .detector_status import DetectorStatus


class VideoInfo:
    
    def __init__(self, id: str, detector_status: DetectorStatus):
        self.id = id
        self.detector_status = detector_status