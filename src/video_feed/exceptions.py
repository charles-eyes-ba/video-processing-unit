class VideoFeedCouldNotConntect(Exception):
    """ Video Feed Could Not Connect """
    def __init__(self, message):
        """
        Parameters
        ----------
        message : str
            The message with error details
        """
        self.message = message


class VideoFeedConnectionLost(Exception):
    """ Video Feed Connection Lost """
    def __init__(self, message):
        """
        Parameters
        ----------
        message : str
            The message with error details
        """
        self.message = message