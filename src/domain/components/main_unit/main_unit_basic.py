from src.models.video_feed import VideoFeed
from src.models.video_info import VideoInfo
from src.dependency_injector import DependencyInjector
from src.domain.components.tracked_video import TrackedVideo
from src.common.logger import logger
from src.common.call import call


class MainUnitBasic:
    
    @property
    def videos_infos(self) -> list[VideoInfo]:
        infos = []
        for tracked_video in self._tracked_videos:
            infos.append(VideoInfo(tracked_video.video_feed.id, tracked_video.video_detector_status))
        return infos
        
    
    def __init__(self, dependencies: DependencyInjector):
        self._dependencies = dependencies
        self._tracked_videos: list[TrackedVideo] = []
        self._on_object_detection = None
        self._on_error = None
        logger.debug('initialized')
    
    
    def setup_callbacks(self, on_object_detection, on_error):
        self._on_object_detection = on_object_detection
        self._on_error = on_error
    
    
    # * Callbacks Handlers
    def _tracked_video_object_detection(self, id: str, objects: list[str]):
        call(self._on_object_detection, id, objects)
        
        
    def _tracked_video_error(self, id: str, error: Exception):
        call(self._on_error, id, error)
    
    
    # * Handle Tracked Videos
    def update_tracked_videos(self, video_feed_list: list[VideoFeed]):
        logger.debug(f'removing {len(self._tracked_videos)} and adding {len(video_feed_list)}')
        self._tracked_videos = []
        for video_feed in video_feed_list:
            self.start_to_track_video(video_feed)


    def start_to_track_video(self, video_feed: VideoFeed):
        logger.debug(f'adding {video_feed.id}')
        if video_feed.id in map(lambda item: item.video_feed.id, self._tracked_videos):
            logger.debug(f'removing old {video_feed.id}')
            self.remove_tracked_video(video_feed.id)
        
        ai_engine = self._dependencies.ai_engine()
        video_capture = self._dependencies.video_capture(video_feed.url)
        video_detector = self._dependencies.video_detector(video_capture, ai_engine)
        tracked_video = self._dependencies.tracked_video(video_feed)
        tracked_video.add_detector(video_detector,
            self._tracked_video_object_detection,
            self._tracked_video_error
        )
        self._tracked_videos.append(tracked_video)
        logger.debug(f'added {video_feed.id}')
        
        
    def remove_tracked_video(self, video_feed_id: str):
        logger.debug(f'removing {video_feed_id}')
        for index, tracked_video in enumerate(self._tracked_videos):
            if tracked_video.video_feed.id == video_feed_id:
                self._tracked_videos[index].stop()
                del self._tracked_videos[index]
                break
        logger.debug(f'removed {video_feed_id}')
