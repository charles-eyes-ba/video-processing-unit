from src.models.video_feed import VideoFeed
from src.models.video_info import VideoInfo
from src.models.video_config import VideoConfig
from src.domain.components.tracked_video import TrackedVideo
from src.common.logger import logger
from src.common.call import call
from .dependencies import MainUnitDependencies


class MainUnitBasic:
    
    @property
    def videos_infos(self) -> list[VideoInfo]:
        infos = []
        for tracked_video in self._tracked_videos:
            infos.append(VideoInfo(tracked_video.id, tracked_video.video_detector_status))
        return infos
        
    
    def __init__(self, dependencies: MainUnitDependencies):
        self._dependencies = dependencies
        self._tracked_videos: list[TrackedVideo] = []
        self._on_object_detection = None
        self._on_error = None
        logger.debug('Initialized')
    
    
    def setup_callbacks(self, on_object_detection, on_error):
        self._on_object_detection = on_object_detection
        self._on_error = on_error
    
    
    # * Callbacks Handlers
    def _tracked_video_object_detection(self, id: str, objects: list[str]):
        call(self._on_object_detection, id, objects)
        
        
    def _tracked_video_error(self, id: str, error: Exception):
        call(self._on_error, id, error)
    
    
    # * Handle Tracked Videos
    def update_tracked_videos(self, video_feed_list: list[(VideoFeed, VideoConfig)]):
        logger.debug(f'Removing {len(self._tracked_videos)} and adding {len(video_feed_list)}')
        self._tracked_videos = []
        for video_feed, video_config in video_feed_list:
            self.start_to_track_video(video_feed, video_config)


    def start_to_track_video(self, video_feed: VideoFeed, video_config: VideoConfig):
        if video_feed.id in map(lambda item: item.id, self._tracked_videos):
            self.remove_tracked_video(video_feed.id)
        tracked_video = self._dependencies.tracked_video(video_feed)
        tracked_video.setup_detector(
            self._tracked_video_object_detection,
            self._tracked_video_error
        )
        tracked_video.set_config(video_config)
        self._tracked_videos.append(tracked_video)
        logger.debug(f'Added {video_feed.id}')
        
        
    def remove_tracked_video(self, video_feed_id: str):
        for index, tracked_video in enumerate(self._tracked_videos):
            if tracked_video.id == video_feed_id:
                self._tracked_videos[index].stop()
                del self._tracked_videos[index]
                logger.debug(f'Removed {video_feed_id}')
                break
        
        
    def update_tracked_video_config(self, video_feed_id: str, video_config: VideoConfig):
        for index, tracked_video in enumerate(self._tracked_videos):
            if tracked_video.id == video_feed_id:
                self._tracked_videos[index].set_config(video_config)
                break
