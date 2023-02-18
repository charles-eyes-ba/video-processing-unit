from numpy import ndarray
from abc import ABC, abstractmethod


class AIEngine(ABC):
    """ Interface to provide methods to execute AI algorithms """

    @abstractmethod
    def extract_objects(self, image: ndarray) -> list[str]:
        """ 
        Predict objects in image 
        
        Parameters
        ----------
        image : numpy.ndarray or str
            Image path to load with OpenCV or the image itself
            
        Returns
        -------
        list[str]
            List with all objects found
        """
        raise NotImplementedError('AIEngine.extract_objects is an abstract method')