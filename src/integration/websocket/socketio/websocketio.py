import socketio
from src.common.logger import logger
from src.common.call import call
from src.domain.dependencies.websocket import WebSocket
from .namespaces.root_namespace import RootNamespace


class WebSocketIO(WebSocket):
    
    def __init__(self, server_url : str):
        self._server_url = server_url
        self._on_connect_callback = None
        self._on_connect_error_callback = None
        self._on_disconnect_callback = None
        self._on_request_current_video_feed_list_callback = None
        self._on_video_feed_list_update_callback = None
        self._on_add_video_feed_callback = None
        self._on_remove_video_feed_callback = None
        
        self._root_namespace = self._generate_root_namespace()
        self._socketio = socketio.Client()
        self._socketio.register_namespace(self._root_namespace)
        logger.debug('WebSocketIO:initialized')


    # * Utils
    def _generate_root_namespace(self):
        """ Generate the config namespace """
        root_namespace = RootNamespace()
        root_namespace.setup_callbacks(
            on_connect=self._on_connect, 
            on_connect_error=self._on_connect_error, 
            on_disconnect=self._on_disconnect, 
            on_request_current_video_feed_list=self._on_request_current_video_feed_list,
            on_video_feed_list_update=self._on_video_feed_list_update,
            on_add_video_feed=self._on_add_video_feed,
            on_remove_video_feed=self._on_remove_video_feed
        )
        return root_namespace


    # * Setup
    def setup_callbacks(
        self, 
        on_connect=None, 
        on_connect_error=None, 
        on_disconnect=None, 
        on_request_current_video_feed_list=None,
        on_video_feed_list_update=None, 
        on_add_video_feed=None, 
        on_remove_video_feed=None
    ):
        self._on_connect_callback = on_connect
        self._on_connect_error_callback = on_connect_error
        self._on_disconnect_callback = on_disconnect
        self._on_request_current_video_feed_list_callback = on_request_current_video_feed_list
        self._on_video_feed_list_update_callback = on_video_feed_list_update
        self._on_add_video_feed_callback = on_add_video_feed
        self._on_remove_video_feed_callback = on_remove_video_feed
      
      
    # * Interface to Handle
    def connect(self):
        self._socketio.connect(self._server_url)
        logger.debug('WebSocketIO:Connected to websocket')
        

    # * Send Methods
    def send_current_video_feed_list(self, video_feed_ids: list[str]):
        try:
            self._root_namespace.emit(RootNamespace.VIDEO_FEED_IDS, { 'ids': video_feed_ids })
            logger.error(f'WebSocketIO:Detect message with this {video_feed_ids} was sent')
        except:
            logger.error('WebSocketIO:Error sending detections')
    
    
    def send_detections(self, id, objects):
        try:
            self._root_namespace.emit(RootNamespace.DETECT, { 'id': id, 'objects': objects })
            logger.error(f'WebSocketIO:Detect message about {id} was sent')
        except:
            logger.error('WebSocketIO:Error sending detections')
    
    
    def send_error(self, id, error):
        try:
            self._root_namespace.emit(RootNamespace.ERROR, { 'id': id, 'error': error.message })
            logger.error(f'WebSocketIO:Error message about {id} was sent')
        except:
            logger.error('WebSocketIO:Error sending error')
    

    # * Receive Events
    def _on_connect(self):
        """ On connect event """
        logger.debug('WebSocketIO:Connected event')
        call(self._on_connect_callback)
        
        
    def _on_connect_error(self):
        """ On connect error event """
        logger.debug('WebSocketIO:Connect error event')
        call(self._on_connect_error_callback)


    def _on_disconnect(self):
        """ On disconnect event """
        logger.debug('WebSocketIO:Disconnected event')
        call(self._on_disconnect_callback)
        
        
    def _on_request_current_video_feed_list(self):
        """ On request current video feed list event """
        logger.debug('WebSocketIO:Current video feed list requested')
        call(self._on_request_current_video_feed_list_callback)
        
    
    def _on_video_feed_list_update(self, data):
        """ 
        On receive configs from server 
        
        Parameters
        ----------
        data : dict
            All video feeds configs
        """
        logger.debug('WebSocketIO:New feed list event')
        call(self._on_video_feed_list_update_callback, data)
            
            
    def _on_add_video_feed(self, data):
        """ 
        On add a video feed to the server 
        
        Parameters
        ----------
        data : dict
            The video feed to add
        """
        logger.debug('WebSocketIO:Add video feed event')
        call(self._on_add_video_feed_callback, data)
            
            
    def _on_remove_video_feed(self, data):
        """ 
        On remove a video feed from the server 
        
        Parameters
        ----------
        data : dict
            The id of the video feed to remove
        """
        logger.debug('WebSocketIO:Remove video feed event')
        call(self._on_remove_video_feed_callback, data)