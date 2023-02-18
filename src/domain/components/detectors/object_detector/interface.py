from abc import ABC, abstractmethod
from src.common.abstract_attribute import abstract_attribute
from src.domain.components.detectors import Detector


class ObjectDetector(Detector, ABC):
    """ Video scanner to find objects """
    
    @abstract_attribute
    def id(self) -> str:
        """ ID (same of video_feed.id) """
        raise NotImplementedError('id() must be defined')
    
    
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