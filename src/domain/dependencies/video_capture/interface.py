from numpy import ndarray
from abc import ABC, abstractmethod

class VideoCapture(ABC):
    """ Class to get video frames from a source """
    
    @abstractmethod
    def setup_callbacks(self, on_error = None):
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
        """ Start the video capture """
        raise NotImplementedError('start() not implemented')
    
    
    @abstractmethod
    def pause(self):
        """ Pause the video capture """
        raise NotImplementedError('pause() not implemented')
    
    
    @abstractmethod
    def stop(self):
        """ Stop the video capture """
        raise NotImplementedError('stop() not implemented')
    
    
    @abstractmethod
    def lastest_frame(self) -> ndarray:
        """ 
        Get the lastest frame 
        
        Returns
        -------
        numpy.ndarray
            Lastest frame
        """
        raise NotImplementedError('lastest_frame() not implemented')