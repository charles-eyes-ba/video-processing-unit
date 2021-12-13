from abc import ABC, abstractmethod
from src.common.abstract_attribute import abstract_attribute

class WebSocket(ABC):
    """ Class that handles the websocket connection """

    # * Attributes
    @abstract_attribute
    def on_video_feeds_update(self):
        """ Function that is called when the all video feeds are updated """
        raise NotImplementedError('on_video_feeds_update must be defined')

    @abstract_attribute
    def on_add_video_feed(self):
        """ Function that is called when a new video feed is added """
        raise NotImplementedError('on_add_video_feed must be defined')

    @abstract_attribute
    def on_remove_video_feed(self):
        """ Function that is called when a video feed is removed """
        raise NotImplementedError('on_remove_video_feed must be defined')

    @abstract_attribute
    def root_namespace(self):
        """ The root namespace. Can be used to send messages in websocket with root namespace  """
        raise NotImplementedError('root_namespace must be defined')

    @abstract_attribute
    def detection_namespace(self):
        """ The detection namespace. Can be used to send messages in websocket with detection namespace """
        raise NotImplementedError('detection_namespace must be defined')

    @abstract_attribute
    def config_namespace(self):
        """ The config namespace. Can be used to send messages in websocket with config namespace """
        raise NotImplementedError('config_namespace must be defined')


    # * Methods
    @abstractmethod
    def setup_callbacks(self, on_video_feeds_update=None, on_add_video_feed=None, on_remove_video_feed=None):
        """ 
        Setup the callbacks 
        
        Parameters
        ----------
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