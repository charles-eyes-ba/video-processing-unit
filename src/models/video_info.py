from .video_status import VideoStatus


class VideoInfo:
    
    def __init__(self, id: str, detector_status: VideoStatus):
        self.id = id
        self.detector_status = detector_status