from src.models.video_feed import VideoFeed
from src.models.video_info import VideoInfo
from src.models.video_config import VideoConfig
from src.domain.components.tracked_video import TrackedVideo
from src.common.logger import logger
from .dependencies import MainUnitDependencies


class MainUnitBasic:
    
    @property
    def videos_infos(self) -> list[VideoInfo]:
        infos = []
        for tracked_video in self._tracked_videos:
            infos.append(VideoInfo(
                tracked_video.id,
                tracked_video.frame_collector_status,
                tracked_video.object_detector_status
            ))
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
            self._on_object_detection,
            self._on_error
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
                logger.debug(f'Updated {video_feed_id}')
                break
