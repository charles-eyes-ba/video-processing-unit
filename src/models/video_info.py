from .detector_status import DetectorStatus


class VideoInfo:
    
    def __init__(
        self, 
        id: str, 
        frame_collector_status: DetectorStatus,
        object_detector_status: DetectorStatus
    ):
        self.id = id
        self.frame_collector_status = frame_collector_status
        self.object_detector_status = object_detector_status