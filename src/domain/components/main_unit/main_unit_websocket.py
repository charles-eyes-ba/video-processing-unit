from src.domain.components.main_unit import MainUnit
from src.domain.dependencies.websocket import WebSocket
from src.models.video_feed import VideoFeed

from src.common.logger import logger


class MainUnitWebSocket:
    
    def __init__(self, websocket: WebSocket):
        self._main_unit = MainUnit()
        self._websocket = websocket
        self._video_detector_list = []
        
        self._websocket.setup_callbacks(
            on_connect=self._on_connect,
            on_connect_error=self._on_connect_error,
            on_disconnect=self._on_disconnect,
            on_request_current_video_feed_list=self._on_request_current_video_feed_list,
            on_video_feeds_update=self._on_video_feeds_update,
            on_add_video_feed=self._on_add_video_feed,
            on_remove_video_feed=self._on_remove_video_feed
        )
        
        logger.debug('MainUnitImpl:initialized')
    
    
    # * WebSocket Deletage
    def _on_connect(self):
        logger.debug('MainUnitWebSocket:connected')
    
    
    def _on_connect_error(self, data):
        logger.debug('MainUnitWebSocket:conection error')
    
    
    def _on_disconnect(self):
        logger.debug('MainUnitWebSocket:disconnected')
        self._websocket.reconnect()
    
    
    def _on_request_current_video_feed_list(self):
        ids = self._main_unit.video_feed_ids
        self._websocket.send_current_video_feed_list(ids)
    
    
    def _on_video_feeds_update(self, data):
        pass
    
    
    def _on_add_video_feed(self, data: dict):
        if data.get('id') is None or data.get('url') is None:
            return
        video_feed = VideoFeed(id=data['id'], url=data['url'])
        self._main_unit.add_video_feed(video_feed)
    
    
    def _on_remove_video_feed(self, data):
        if data.get('id') is None:
            return
        self._main_unit.remove_video_feed(data['id'])