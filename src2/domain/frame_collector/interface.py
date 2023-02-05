from abc import ABC, abstractmethod

class FrameCollector(ABC):
    """ Class that wraps a video capture object and provides a lastest frame """
    
    @abstractmethod
    def __init__(self, video_capture):
        """
        Parameters
        ----------
        video_capture : VideoCapture
            Video capture object
        """
        raise NotImplementedError('__init__() not implemented')
        
        
    @abstractmethod
    def setup_callbacks(self, on_error=None):
        """ 
        Setup the callbacks 
        
        Parameters
        ----------
        on_error : function
            Function to be called when the vide capture receive an error. 
            The function must have the following signature: function(exception).
        """
        raise NotImplementedError('setup_callbacks() not implemented')
        
      
    @abstractmethod
    def start(self):
        """ Start the frame collector """
        raise NotImplementedError('start() not implemented')
    
    
    @abstractmethod
    def stop(self):
        """ Stop the frame collector """
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
        """ Release the video capture and frame collector """
        raise NotImplementedError('release() not implemented')