class InvalidDeepNeuralNetworkFilesException(Exception):
    """ Exception for invalid Deep Neural Network files """
    def __init__(self, message):
        """
        Parameters
        ----------
        message : str
            The message with error details
        """
        self.message = message