from abc import ABC, abstractmethod

class VideoCapture(ABC):
    """ Abstract class to get video frames from a source """
    
    @abstractmethod
    def __init__(self, path):
        raise NotImplementedError('__init__() not implemented')
        
    @abstractmethod
    def read(self):
        """ 
        Returns the next frame from the source 
        
        Returns
        -------
        numpy.ndarray
            The next frame from the source
        """
        raise NotImplementedError('read() not implemented')