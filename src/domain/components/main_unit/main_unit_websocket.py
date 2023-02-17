import time
import signal
from src.domain.components.main_unit import MainUnit
from src.models.video_feed import VideoFeed
from src.models.video_config import VideoConfig
from src.common.dict_encoder import DictEncoder
from .dependencies import MainUnitDependencies
from src.common.logger import logger
from src.common.check_keys import check_keys


class MainUnitWebSocket:
    
    def __init__(self, dependencies: MainUnitDependencies):
        self._dependencies = dependencies
        self._main_unit = MainUnit(dependencies)
        self._websocket = self._dependencies.websocket()
        self._websocket_delay_retry = 30
        self._video_detector_list = []
        
        self._websocket.setup_callbacks(
            on_connect=self._on_connect,
            on_connect_error=self._on_connect_error,
            on_disconnect=self._on_disconnect,
            on_request_current_video_feed_list=self._on_request_current_video_feed_list,
            on_video_feed_list_update=self._on_video_feed_list_update,
            on_add_video_feed=self._on_add_video_feed,
            on_remove_video_feed=self._on_remove_video_feed,
            on_update_video_feed_config=self._on_update_video_feed_config
        )
        logger.debug('Initialized')
    
    
    # * Interfaces
    def start(self):
        self._websocket.connect()
        signal.pause()
    
    
    # * WebSocket Deletage
    def _on_connect(self):
        logger.debug('Connected to the websocket server')
    
    
    def _on_connect_error(self):
        logger.debug(f'Trying to connect to websocket again in {self._websocket_delay_retry} seconds...')
        time.sleep(self._websocket_delay_retry)
        self._websocket.connect()
    
    
    def _on_disconnect(self):
        logger.debug(f'Disconnected from the websocket server.')
    
    
    def _on_request_current_video_feed_list(self):
        logger.debug('Request the current videos infos')
        videos = DictEncoder.encode(self._main_unit.videos_infos)
        self._websocket.send_current_videos_infos(videos)
    
    
    def _on_video_feed_list_update(self, data: list):
        logger.debug('New video feed list')
        video_feed_list = []
        for dictionary in data:
            if not check_keys(dictionary, keys=['id', 'url', 'config']) or not check_keys(dictionary.get('config'), keys=['run_detector']):
                return
            
            video_feed = VideoFeed(id=dictionary['id'], url=dictionary['url'])
            video_config = VideoConfig(run_detector=dictionary['config']['run_detector'])
            video_feed_list.append((video_feed, video_config))
        self._main_unit.update_tracked_videos(video_feed_list)
    
    
    def _on_add_video_feed(self, data: dict):
        logger.debug('Add a new video feed')
        if not check_keys(data, keys=['id', 'url', 'config']) or not check_keys(dictionary=data.get('config'), keys=['run_detector']):
            logger.error(f'invalid data')
            return
        
        video_feed = VideoFeed(id=data['id'], url=data['url'])
        video_config = VideoConfig(run_detector=data['config']['run_detector'])
        self._main_unit.start_to_track_video(video_feed, video_config)
    
    
    def _on_remove_video_feed(self, data):
        logger.debug('Remove a video feed')
        if not check_keys(dictionary=data, keys=['id']):
            logger.error(f'invalid data')
            return
        self._main_unit.remove_tracked_video(data['id'])
        
        
    def _on_update_video_feed_config(self, data):
        logger.debug('Update a video feed config')
        if not check_keys(dictionary=data, keys=['id', 'config']) or not check_keys(dictionary=data.get('config'), keys=['run_detector']):
            logger.error(f'invalid data')
            return
        video_config = VideoConfig(run_detector=data['config']['run_detector'])
        self._main_unit.update_tracked_video_config(data['id'], video_config)