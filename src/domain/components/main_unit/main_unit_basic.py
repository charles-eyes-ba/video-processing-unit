from src.factory import Factory
from src.models.video_feed import VideoFeed

from src.common.logger import logger


class MainUnitBasic:
    
    @property
    def video_feed_ids(self) -> list[str]:
        ids = []
        for video_detector in self._video_detector_list:
            ids.append(video_detector.id)
        return ids
    
    
    def __init__(self):
        self._video_detector_list = []
        self._on_detection_callback = None
        self._on_error_callback = None
        logger.debug('MainUnitImpl:initialized')
    
    
    def setup_callbacks(self, on_detection = None, on_error = None):
        self._on_detection_callback = on_detection
        self._on_error_callback = on_error
    
    
    def update_video_feed_list(self, video_feed_list: list[VideoFeed]):
        logger.debug(f'MainUnitImpl:removing {len(self._video_detector_list)} feeds and adding {len(video_feed_list)}')
        self._video_detector_list = []
        for video_feed in video_feed_list:
            self.add_video_feed(video_feed)


    def add_video_feed(self, video_feed: VideoFeed):
        ai_engine = Factory.ai_engine()
        video_capture = Factory.video_capture(video_feed.url)
        video_detector = Factory.video_detector(video_feed.id, video_capture, ai_engine)
        
        video_detector.start()
        self._video_detector_list.append(video_detector)
        logger.debug(f'MainUnitImpl:added {video_feed.id}')

        
    def remove_video_feed(self, video_feed_id: str):
        for video_detector in self._video_detector_list:
            if video_detector.id == video_feed_id:
                del video_detector
                break
        logger.debug(f'MainUnitImpl:removed {video_feed_id}')