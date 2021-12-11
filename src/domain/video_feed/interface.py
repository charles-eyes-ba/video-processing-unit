from abc import ABC, abstractmethod
from src.common.abstract_attribute import abstract_attribute

class VideoFeed(ABC):
    """
    Class that wraps a video capture object and provides a lastest frame. It starts a thread that updates the lastest frame.
    """
    @abstractmethod
    def __init__(self, video_capture):
        """
        Parameters
        ----------
        id : str
            Id of the video feed
        video_capture : VideoCapture
            Video capture object
        on_error : function
            Function to be called when the video feed receive an error
        """
        raise NotImplementedError('__init__() not implemented')
        
        
    @abstractmethod
    def setup_callbacks(self, on_error=None):
        """ 
        Setup the callbacks 
        
        Parameters
        ----------
        on_error : function
            Function to be called when the video feed receive an error. 
            The function must have the following signature: function(exception). 
            Exception is a VideoFeedCouldNotConntect or VideoFeedConnectionLost.
        """
        raise NotImplementedError('setup_callbacks() not implemented')
        
      
    @abstractmethod
    def start(self):
        """ Start the video feed """
        raise NotImplementedError('start() not implemented')
    
    
    @abstractmethod
    def stop(self):
        """ Stop the video feed """
        raise NotImplementedError('stop() not implemented')
    
    
    @abstractmethod
    def pop_lastest_frame(self):
        """ 
        Pop the lastest frame 
        
        Returns
        -------
        numpy.ndarray
            Lastest frame
        """
        raise NotImplementedError('pop_lastest_frame() not implemented')
    
    
    @abstractmethod
    def release(self):
        """ Release the video capture object """
        raise NotImplementedError('release() not implemented')