import time
import signal
from src.dependency_injector import DependencyInjector
from src.domain.components.main_unit import MainUnit
from src.models.video_feed import VideoFeed
from src.common.logger import logger
from src.common.check_keys import check_keys


class MainUnitWebSocket:
    
    def __init__(self, dependencies: DependencyInjector):
        self._dependencies = dependencies
        self._main_unit = MainUnit(dependencies)
        self._websocket = self._dependencies.websocket()
        self._websocket_delay_retry = 5
        self._video_detector_list = []
        
        self._websocket.setup_callbacks(
            on_connect=self._on_connect,
            on_connect_error=self._on_connect_error,
            on_disconnect=self._on_disconnect,
            on_request_current_video_feed_list=self._on_request_current_video_feed_list,
            on_video_feed_list_update=self._on_video_feed_list_update,
            on_add_video_feed=self._on_add_video_feed,
            on_remove_video_feed=self._on_remove_video_feed
        )
        logger.debug('Initialized')
    
    
    # * Interfaces
    def start(self):
        self._websocket.connect()
        signal.pause()
    
    
    # * WebSocket Deletage
    def _on_connect(self):
        pass
    
    
    def _on_connect_error(self):
        logger.info(f'Trying to connect to websocket again in {self._websocket_delay_retry} seconds...')
        time.sleep(self._websocket_delay_retry)
        self._websocket.connect()
    
    
    def _on_disconnect(self):
        self._websocket.connect()
    
    
    def _on_request_current_video_feed_list(self):
        logger.debug(self._main_unit.videos)
    
    
    def _on_video_feed_list_update(self, data: list):
        video_feed_list = []
        for dictionary in data:
            if not check_keys(dictionary, keys=['id', 'url']):
                return
            video_feed_list.append(VideoFeed(dictionary['id'], dictionary['url']))
        self._main_unit.update_tracked_videos(video_feed_list)
    
    
    def _on_add_video_feed(self, data: dict):
        if not check_keys(dictionary=data, keys=['id', 'url']):
            logger.error(f'invalid data')
            return
        video_feed = VideoFeed(data['id'], data['url'])
        self._main_unit.start_to_track_video(video_feed)
    
    
    def _on_remove_video_feed(self, data):
        if not check_keys(dictionary=data, keys=['id']):
            logger.error(f'invalid data')
            return
        self._main_unit.remove_tracked_video(data['id'])