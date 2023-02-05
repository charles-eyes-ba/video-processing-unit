from abc import ABC, abstractmethod
from src.common.abstract_attribute import abstract_attribute

class VideoDetector(ABC):
    """ Class that make detections in a image. """
    
    @abstract_attribute
    def id(self):
        """ The id of the video detector """
        raise NotImplementedError('id must be defined')


    @abstractmethod
    def setup_callbacks(self, on_object_detection = None, on_error = None):
        """
        Setup the callbacks
        
        Parameters
        ----------
        on_object_detection : function
            The function to call when an object is detected. The function must have the following signature: function(camera_id, classes)
        on_error : function
            The function to call when an error occurs. The function must have the following signature: function(camera_id, exception)
        """
        raise NotImplementedError('setup_callbacks() not implemented')


    @abstractmethod
    def start(self):
        """ Start the detector """
        raise NotImplementedError('start() not implemented')
        
    
    @abstractmethod
    def stop(self):
        """ Stop the detector """
        raise NotImplementedError('stop() not implemented')
    
    
    @abstractmethod
    def pause(self):
        """ Pause the detector """
        raise NotImplementedError('pause() not implemented')