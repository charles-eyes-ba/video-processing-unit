from src.models.video_feed import VideoFeed
from src.dependency_injector import DependencyInjector
from src.common.logger import logger


class MainUnitBasic:
    
    def __init__(self, dependencies: DependencyInjector):
        self._dependencies = dependencies
        self._tracked_videos = []
        self._on_detection_callback = None
        self._on_error_callback = None
        logger.debug('MainUnitImpl:initialized')
    
    
    def setup_callbacks(self, on_detection = None, on_error = None):
        self._on_detection_callback = on_detection
        self._on_error_callback = on_error
    
    
    def update_tracked_videos(self, video_feed_list: list[VideoFeed]):
        logger.debug(f'MainUnitImpl:removing {len(self._tracked_videos)} and adding {len(video_feed_list)}')
        self._tracked_videos = []
        for video_feed in video_feed_list:
            self.start_video_track(video_feed)


    def start_video_track(self, video_feed: VideoFeed):
        
        
        video_detector.start()
        self._video_detector_list.append(video_detector)
        logger.debug(f'MainUnitImpl:added {video_feed.id}')

        
    def remove_tracked_video(self, video_feed_id: str):
        for index, video_detector in enumerate(self._video_detector_list):
            if video_detector.id == video_feed_id:
                del self._video_detector_list[index]
                break
        logger.debug(f'MainUnitImpl:removed {video_feed_id}')