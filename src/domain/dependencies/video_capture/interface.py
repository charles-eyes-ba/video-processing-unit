from numpy import ndarray
from abc import ABC, abstractmethod
from src.common.abstract_attribute import abstract_attribute


class VideoCapture(ABC):
    """ Class to get video frames from a source """
    
    @abstract_attribute
    def url(self) -> str:
        """ Video feed URL """
        raise NotImplementedError('url() must be defined')
    
    
    @abstractmethod
    def __init__(self, url: str):
        """
        Initializer
        
        Parameters
        ----------
        url : str
            URL to retrive the video
        """
        raise NotImplementedError('__init__(url:) not implemented')
    
    
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