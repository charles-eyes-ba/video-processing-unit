class VideoCaptureConnectionLost(Exception):
    """ Video capture connection lost """
    def __init__(self, message):
        """
        Parameters
        ----------
        message : str
            The message with error details
        """
        self.message = message