from src.models.video_feed import VideoFeed
from src.models.video_config import VideoConfig
from src.models.detector_status import DetectorStatus
from src.domain.components.detectors import Detector
from src.common.logger import logger
from src.common.call import call
from .interface import TrackedVideo
from .dependencies import TrackedVideoDependencies


class TrackedVideoImpl(TrackedVideo):
    
    @property
    def id(self) -> str:
        return self._video_feed.id
    
    
    # * Status
    @property
    def video_detector_status(self) -> DetectorStatus:
        return self._video_detector_status
    
    
    # * Init
    def __init__(
        self, 
        dependencies: TrackedVideoDependencies, 
        video_feed: VideoFeed
    ):
        self._dependencies = dependencies
        self._video_feed = video_feed
        self._video_config = VideoConfig.all_disabled()
        self._detectors: list[Detector] = []
        
        self._ai_engine = self._dependencies.ai_engine()
        self._video_capture = self._dependencies.video_capture(self._video_feed.id, self._video_feed.url)
        
        self._video_detector = self._dependencies.object_detector(self._video_feed.id, self._video_capture, self._ai_engine)
        self._video_detector_status = DetectorStatus.OFF
        self._detectors.append(self._video_detector)
        
        logger.debug('Initialized')
        
        
    def _update_detector(self, should_run: bool ,detector: Detector) -> DetectorStatus:
        if should_run:
            detector.start()
            return DetectorStatus.RUNNING
        else:
            detector.stop()
            return DetectorStatus.OFF
        
        
    # * Interfaces
    def set_config(self, config: VideoConfig):
        logger.debug(f'New config received {config.__dict__}')
        self._video_config = config
        
        if not self._video_config.run_frame_collector:
            _ = [detector.stop() for detector in self._detectors]
            self._video_capture.stop()
            return
        
        self._video_capture.start()    
        self._video_detector_status = self._update_detector(self._video_config.run_object_detector, self._video_detector)
        
    
    def stop(self):
        logger.debug('Stopping')
        self._video_detector.stop()
        
        
    # * Detector
    def setup_detector(self, on_object_detection, on_error):
        logger.debug('Adding detector')
        def _object_detection(objects: list[str]):
            call(on_object_detection, self._video_feed.id, objects)
            
        def _error(error: Exception):
            self._video_detector.stop()
            self._video_detector_status = DetectorStatus.ERROR
            call(on_error, self._video_feed.id, error)
            
        self._video_detector.setup_callbacks(
            _object_detection,
            _error
        )