from abc import ABC, abstractmethod

class WebSocket(ABC):
    """ Class that handles the websocket connection """

    @abstractmethod
    def setup_callbacks(
        self, 
        on_connect: function = None, 
        on_connect_error: function = None, 
        on_disconnect: function = None, 
        on_video_feeds_update: function = None, 
        on_add_video_feed: function = None, 
        on_remove_video_feed: function = None
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
        on_video_feeds_update : function
            Function that is called when the all video feeds are updated
        on_add_video_feed : function
            Function that is called when a new video feed is added
        on_remove_video_feed : function
            Function that is called when a video feed is removed
        """
        raise NotImplementedError('setup_callbacks() must be implemented')
    

    @abstractmethod
    def connect(self, url):
        """
        Connect to the websocket server
        
        Parameters
        ----------
        url : str
            The url of the websocket server
        """
        raise NotImplementedError('connect() must be implemented')
        

    @abstractmethod
    def request_configs(self):
        """ Request configs from server """
        raise NotImplementedError('request_configs() must be implemented')


    @abstractmethod
    def send_detections(self, id, classes):
        """ 
        Send detections to server 
        
        Parameters
        ----------
        id : str
            The id of the video feed
        classes : list
            The classes name detected in the video feed
        """
        raise NotImplementedError('send_detections() must be implemented')
    
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