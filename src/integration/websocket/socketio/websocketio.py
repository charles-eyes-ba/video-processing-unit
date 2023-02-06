import logging
import socketio
from time import sleep

from src2.common.call import call
from src2.domain.websocket import WebSocket
from .namespaces.root_namespace import RootNamespace

class WebSocketIO(WebSocket):
    
    def __init__(self, server_url):
        self._server_url = server_url
        self._on_connect_callback = None
        self._on_connect_error_callback = None
        self._on_disconnect_callback = None
        self._on_video_feeds_update_callback = None
        self._on_add_video_feed_callback = None
        self._on_remove_video_feed_callback = None
        
        self._root_namespace = self._generate_root_namespace()

        self._socketio = socketio.Client()
        self._socketio.register_namespace(self._root_namespace)
        logging.info('WebSocketIO:initialized')
        
        self._connect()


    # * Utils
    def _generate_root_namespace(self):
        """ Generate the config namespace """
        root_namespace = RootNamespace()
        root_namespace.setup_callbacks(
            on_connect=self._on_connect, 
            on_connect_error=self._on_connect_error, 
            on_disconnect=self._on_disconnect, 
            on_video_feed_list_update=self._on_video_feed_list_update,
            on_add_video_feed=self._on_add_video_feed,
            on_remove_video_feed=self._on_remove_video_feed
        )
        return root_namespace


    def _connect(self):
        delay_to_retry = 5
        while True:
            try:
                self._socketio.connect(self._server_url)
                logging.info('WebSocketIO:Connected to websocket')
                break
            except:
                logging.info(f'WebSocketIO:Trying to connect to websocket again in {delay_to_retry} seconds...')
                sleep(delay_to_retry)


    # * Setup
    def setup_callbacks(
        self, 
        on_connect=None, 
        on_connect_error=None, 
        on_disconnect=None, 
        on_video_feeds_update=None, 
        on_add_video_feed=None, 
        on_remove_video_feed=None
    ):
        self._on_connect_callback = on_connect
        self._on_connect_error_callback = on_connect_error
        self._on_disconnect_callback = on_disconnect
        self._on_video_feeds_update_callback = on_video_feeds_update
        self._on_add_video_feed_callback = on_add_video_feed
        self._on_remove_video_feed_callback = on_remove_video_feed
        

    # * Send Methods
    def send_detections(self, id, objects):
        try:
            self._root_namespace.emit(RootNamespace.DETECT, { 'id': id, 'objects': objects })
            logging.error(f'WebSocketIO:Detect message about {id} was sent')
        except:
            logging.error('WebSocketIO:Error sending detections')
    
    
    def send_error(self, id, error):
        try:
            self._root_namespace.emit(RootNamespace.ERROR, { 'id': id, 'error': error.message })
            logging.error(f'WebSocketIO:Error message about {id} was sent')
        except:
            logging.error('WebSocketIO:Error sending error')
    

    # * Receive Events
    def _on_connect(self):
        """ On connect event """
        logging.debug('WebSocketIO:Connected event')
        call(self._on_connect_callback)
        
        
    def _on_connect_error(self, data):
        """ On connect error event """
        logging.debug('WebSocketIO:Connect error event')
        call(self._on_connect_error_callback)


    def _on_disconnect(self):
        """ On disconnect event """
        logging.debug('WebSocketIO:Disconnected event')
        call(self._on_disconnect_callback)
        
    
    def _on_video_feed_list_update(self, config):
        """ 
        On receive configs from server 
        
        Parameters
        ----------
        config : dict
            All video feeds configs
        """
        logging.debug('WebSocketIO:New feed list event')
        call(self._on_video_feeds_update_callback, config['cameras'])
            
            
    def _on_add_video_feed(self, video_feed):
        """ 
        On add a video feed to the server 
        
        Parameters
        ----------
        video_feed : dict
            The video feed to add
        """
        logging.debug('WebSocketIO:Add video feed event')
        call(self._on_add_video_feed_callback, video_feed)
            
            
    def _on_remove_video_feed(self, video_feed_id):
        """ 
        On remove a video feed from the server 
        
        Parameters
        ----------
        video_feed_id : str
            The id of the video feed to remove
        """
        logging.debug('WebSocketIO:Remove video feed event')
        call(self._on_remove_video_feed_callback, video_feed_id)