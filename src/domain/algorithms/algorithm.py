from abc import ABC, abstractmethod

class Algorithm(ABC):
    """
    Abstract class for all algorithms
    """
    @abstractmethod
    def run(self, boxes, scores, classes):
        """
        Runs the algorithm.
        """
        raise NotImplementedError("run() is not implemented.")