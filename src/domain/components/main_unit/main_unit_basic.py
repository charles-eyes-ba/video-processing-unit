from src.models.video_feed import VideoFeed
from src.dependency_injector import DependencyInjector
from src.domain.components.tracked_video import TrackedVideo
from src.common.logger import logger


class MainUnitBasic:
    
    def __init__(self, dependencies: DependencyInjector):
        self._dependencies = dependencies
        self._tracked_videos: list[TrackedVideo] = []
        logger.debug('MainUnitImpl:initialized')
    
    
    # * Handle Tracked Videos
    def update_tracked_videos(self, video_feed_list: list[VideoFeed]):
        logger.debug(f'MainUnitImpl:removing {len(self._tracked_videos)} and adding {len(video_feed_list)}')
        self._tracked_videos = []
        for video_feed in video_feed_list:
            self.start_to_track_video(video_feed)


    def start_to_track_video(self, video_feed: VideoFeed):
        ai_engine = self._dependencies.ai_engine()
        video_capture = self._dependencies.video_capture(video_feed.url)
        video_detector = self._dependencies.video_detector(video_capture, ai_engine)
        
        tracked_video = self._dependencies.tracked_video(video_feed)
        tracked_video.add_detector(video_detector,
            on_object_detection = lambda id, objects: logger.debug(f'MainUnitImpl:detection:{id}:{objects}'),
            on_error = lambda id, objects: logger.debug(f'MainUnitImpl:error:{id}:{objects}')
        )
        
        self._tracked_videos.append(tracked_video)
        logger.debug(f'MainUnitImpl:added {video_feed.id}')
        
        
    def remove_tracked_video(self, video_feed_id: str):
        for index, tracked_video in enumerate(self._tracked_videos):
            if tracked_video.video_feed.id == video_feed_id:
                del self._tracked_videos[index]
                break
        logger.debug(f'MainUnitImpl:removed {video_feed_id}')