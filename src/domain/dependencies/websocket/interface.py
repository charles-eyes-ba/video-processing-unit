from abc import ABC, abstractmethod
from src.models.video_feed import VideoFeed

class WebSocket(ABC):
    """ Class that handles the websocket connection """

    @abstractmethod
    def setup_callbacks(
        self, 
        on_connect=None, 
        on_connect_error=None, 
        on_disconnect=None, 
        on_request_current_video_feed_list=None,
        on_video_feeds_update=None, 
        on_add_video_feed=None, 
        on_remove_video_feed=None
    ):
        """ 
        Setup the callbacks 
        
        Parameters
        ----------
        on_connect : function
            Function that is called when the connection is established
        on_connect_error : function
            Function that is called when the connection fails
        on_disconnect : function
            Function that is called when the connection is lost
        on_request_current_video_feed_list : function
            Function that is called when the server request all the current video feeds
        on_video_feeds_update : function
            Function that is called when the all video feeds are updated
        on_add_video_feed : function
            Function that is called when a new video feed is added
        on_remove_video_feed : function
            Function that is called when a video feed is removed
        """
        raise NotImplementedError('setup_callbacks() must be implemented')
    
    
    @abstractmethod
    def connect(self):
        """ Try to connect """
        raise NotImplementedError('connect() must be implemented')
    
    
    @abstractmethod
    def send_current_video_feed_list(self, video_feed_ids: list[str]):
        """ 
        Send the video feed list to server 
        
        Parameters
        ----------
        video_feed_ids : list
            The list with all video feed ids
        """
        raise NotImplementedError('send_current_video_feed_list() must be implemented')
    

    @abstractmethod
    def send_detections(self, id, objects):
        """ 
        Send detections to server 
        
        Parameters
        ----------
        id : str
            The id of the video feed
        objects : list
            The objects names detected in the video feed
        """
        raise NotImplementedError('send_detections() must be implemented')
    
    
    @abstractmethod
    def send_error(self, id, error):
        """ 
        Send error to server 
        
        Parameters
        ----------
        id : str
            The id of the video feed
        error : str
            The error message
        """
        raise NotImplementedError('send_error() must be implemented')