from .video_status import VideoStatus

class VideoInfo:
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def detector_status(self) -> VideoStatus:
        return self._detector_status
    
    def __init__(self, id: str, detector_status: VideoStatus):
        self._id = id
        self._detector_status = detector_status