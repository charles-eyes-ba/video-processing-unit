from abc import ABC, abstractmethod
from src.common.abstract_attribute import abstract_attribute

class VideoFeed(ABC):
    """
    Class that wraps a video capture object and provides a lastest frame. It starts a thread that updates the lastest frame.
    """
    
    @abstract_attribute
    def status():
        """ True if the lastest frame is valid """
        raise NotImplementedError('VideoFeed is an abstract class')

    @abstract_attribute
    def frame():
        """ Lastest frame """
        raise NotImplementedError('VideoFeed is an abstract class')

    @abstract_attribute
    def width():
        """ Width of the video feed """
        raise NotImplementedError('VideoFeed is an abstract class')

    @abstract_attribute
    def height():
        """ Height of the video feed """
        raise NotImplementedError('VideoFeed is an abstract class')

    @abstract_attribute
    def fps():
        """ Frames per second of the video feed """
        raise NotImplementedError('VideoFeed is an abstract class')

    @abstract_attribute
    def is_running():
        """ True if the video feed is running """
        raise NotImplementedError('VideoFeed is an abstract class')

    
    @abstractmethod
    def __init__(self, feed_url):
        """
        Parameters
        ----------
        id : str
            Id of the video feed
        feed_url : str or int
            URL (str) or code (int) to access remote video or local camera
        on_error : function
            Function to be called when the video feed receive an error
        """
        raise NotImplementedError('VideoFeed is an abstract class')
        
        
    @abstractmethod
    def setup_callbacks(self, on_error=None):
        """ 
        Setup the callbacks 
        
        Parameters
        ----------
        on_error : function
            Function to be called when the video feed receive an error. 
            The function must have the following signature: function(camera_id, exception). 
            Exception is a VideoFeedCouldNotConntect or VideoFeedConnectionLost.
        """
        raise NotImplementedError('VideoFeed.setup_callbacks is an abstract class')
        
      
    @abstractmethod
    def start(self):
        """ Start the video feed """
        raise NotImplementedError('VideoFeed.start is an abstract class')
    
    
    @abstractmethod
    def stop(self):
        """ Stop the video feed """
        raise NotImplementedError('VideoFeed.stop is an abstract class')
    
    
    @abstractmethod
    def pop_lastest_frame(self):
        """ 
        Pop the lastest frame 
        
        Returns
        -------
        numpy.ndarray
            Lastest frame
        """
        raise NotImplementedError('VideoFeed.pop_lastest_frame is an abstract class')
    
    
    @abstractmethod
    def release(self):
        """ Release the video capture object """
        raise NotImplementedError('VideoFeed.release is an abstract class')