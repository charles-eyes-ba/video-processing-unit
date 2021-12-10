class CameraParamsNotFoundException(Exception):
    """ Exception for when the camera parameters are not found """
    def __init__(self, message):
        """
        Parameters
        ----------
        message : str
            The message with error details
        """
        self.message = message