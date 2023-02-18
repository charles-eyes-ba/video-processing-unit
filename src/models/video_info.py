from .status import Status


class VideoInfo:
    """ An overview about the video feed and which components are running on it """
    
    def __init__(
        self, 
        id: str, 
        frame_collector_status: Status,
        object_detector_status: Status
    ):
        self.id = id
        self.frame_collector_status = frame_collector_status
        self.object_detector_status = object_detector_status