from abc import ABC, abstractmethod
from src.common.abstract_attribute import abstract_attribute

class MainUnit(ABC):
    """ Class that handles the video processing unit """

    @abstract_attribute
    def video_feed_ids(self) -> list[str]:
        """ The video feed id list """
        raise NotImplementedError('video_feed_ids must be defined')


    @abstractmethod
    def setup_callbacks(self, on_detection = None, on_error = None):
        """
        Setup the callbacks
        
        Parameters
        ----------
        on_detection : function
            The function to call when an object is detected. The function must have the following signature: function(camera_id, classes)
        on_error : function
            The function to call when an error occurs. The function must have the following signature: function(camera_id, exception)
        """
        raise NotImplementedError('setup_callbacks() not implemented')


    @abstractmethod
    def update_video_feed_list(self, video_feed_list):
        """ 
        Updates the list of video feeds to be processed 
        
        Parameters
        ----------
        video_feed_list : list
            The list of video feeds to be processed (replace all current video feeds)
        """
        raise NotImplementedError('update_video_feed_list() not implemented')


    @abstractmethod
    def add_video_feed(self, video_feed):
        """ 
        Adds a video feed to the list of video feeds to be processed 
        
        Parameters
        ----------
        video_feed : VideoFeed
            The video feed to be added
        """
        raise NotImplementedError('add_video_feed() not implemented')


    @abstractmethod
    def remove_video_feed(self, video_feed_id):
        """ 
        Removes a video feed from the list of video feeds to be processed 
        
        Parameters
        ----------
        video_feed_id : int
            The id of the video feed to be removed
        """
        raise NotImplementedError('remove_video_feed() not implemented')