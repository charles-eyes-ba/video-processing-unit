from abc import ABC, abstractmethod

class Request(ABC):
    """ Class that handles http connections """

    @abstractmethod
    def post(self, url: str, body: dict) -> any:
        """
        Send a post request
        
        Parameters
        ----------
        url : str
            The url to hit
        body: dict
            The body to send in the request
            
        Returns
        -------
        any
            Response from the request
        """
        raise NotImplementedError('post() must be implemented')