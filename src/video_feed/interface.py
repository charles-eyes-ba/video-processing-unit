from abc import ABC, abstractmethod

class VideoFeed:
    """
    Class that wraps a video capture object and provides a lastest frame. It starts a thread that updates the lastest frame.
    
    Attributes
    ----------
    id : str
        Id of the video feed
    status : bool
        True if the lastest frame is valid
    frame : numpy.ndarray
        Lastest frame
    width : int
        Width of the video feed
    height : int
        Height of the video feed
    fps : int
        Frames per second of the video feed
    is_running : bool
        True if the video feed is running
    on_error : function
        Function to be called when the video feed receive an error. 
        The function must have the following signature: function(camera_id, exception). 
        Exceptions: VideoFeedCouldNotConntect or VideoFeedConnectionLost.
        
    Methods
    -------
    release()
        Release the video capture object
    pop_lastest_frame()
        Pop the lastest frame
    """
    def __init__(self, id: str, feed_url: str):
        """
        Parameters
        ----------
        id : str
            Id of the video feed
        feed_url : str or int
            URL (str) or code (int) to access remote video or local camera
        on_connection_error : function
            Function to be called when the video feed receive an error
        """
        raise NotImplementedError('VideoFeed is an abstract class')
        
        
    def setup_callbacks(self, on_error: function):
        """ 
        Setup the callbacks 
        
        Parameters
        ----------
        on_error : function
            Function to be called when the video feed receive an error
        """
        raise NotImplementedError('VideoFeed is an abstract class')
    
        
    def pop_lastest_frame(self):
        """ 
        Pop the lastest frame 
        
        Returns
        -------
        numpy.ndarray
            Lastest frame
        """
        raise NotImplementedError('VideoFeed is an abstract class')
    
    
    def release(self):
        """ Release the video capture object """
        raise NotImplementedError('VideoFeed is an abstract class')