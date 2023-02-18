class VideoCaptureCouldNotConnect(Exception):
    """ Video capture could not connect to the camera """
    def __init__(self, message):
        """
        Parameters
        ----------
        message : str
            The message with error details
        """
        self.message = message