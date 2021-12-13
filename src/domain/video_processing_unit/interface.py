from abc import ABC, abstractmethod

class VideoProcessingUnit(ABC):
    """ Class that handles the video processing unit """
    @abstractmethod
    def __init__(self, websocket, create_detector):
        raise NotImplementedError('__init__() not implemented')
            

    @abstractmethod
    def _update_video_feed_list(self, video_feed_list):
        """ 
        Updates the list of video feeds to be processed 
        
        Parameters
        ----------
        video_feed_list : list
            The list of video feeds to be processed (replace all current video feeds)
        """
        raise NotImplementedError('_update_video_feed_list() not implemented')


    @abstractmethod
    def _add_video_feed(self, video_feed):
        """ 
        Adds a video feed to the list of video feeds to be processed 
        
        Parameters
        ----------
        video_feed : VideoFeed
            The video feed to be added
        """
        raise NotImplementedError('_add_video_feed() not implemented')
        

    @abstractmethod
    def _remove_video_feed(self, video_feed_id):
        """ 
        Removes a video feed from the list of video feeds to be processed 
        
        Parameters
        ----------
        video_feed_id : int
            The id of the video feed to be removed
        """
        raise NotImplementedError('_remove_video_feed() not implemented')
    

    @abstractmethod
    def _on_detection_callback(self, id, classes):
        """ 
        Callback for when a detection is made for a video processor
        
        Parameters
        ----------
        id : str
            The id of the video processor
        classes : list
            The list of classes detected
        """
        raise NotImplementedError('_on_detection_callback() not implemented')
    

    @abstractmethod
    def _on_error_callback(self, id, exception):
        """ 
        Callback for when an error is made for a video processor
        
        Parameters
        ----------
        id : str
            The id of the video processor
        exception : Exception
            The exception that was thrown
        """
        raise NotImplementedError('_on_error_callback() not implemented')
    

    @abstractmethod
    def start(self):
        """ Starts video processing unit aplication """
        raise NotImplementedError('start() not implemented')