from abc import ABC, abstractmethod

class DeepNeuralNetwork(ABC):
    """
    Class that handles the detection of objects in an image
    
    Methods
    -------
    predict(image)
        Predict objects in image
    show_img_with_boxes(title, image, boxes, scores, classes, scale=None)
        Show image with boxes
    """
    @abstractmethod
    def __init__(self, config_path, weights_path, classes_path):
        """
        Parameters
        ----------
        config_path : str
            Path to load DNN config file
        weights_path : str
            Path to load DNN weights file
        classes_path : str
            Path to load DNN classes names file
            
        Raises
        ------
        InvalidDeepNeuralNetworkFilesException
            If one of the files to load deep neural network is invalid
        """
        raise NotImplementedError('DeepNeuralNetwork is an abstract class')
    
    
    @abstractmethod
    def predict(self, image):
        """ 
        Predict objects in image 
        
        Parameters
        ----------
        image : numpy.ndarray or str
            Image path to load with OpenCV or the image itself
            
        Returns
        -------
        tuple
            Tuple with all detections filtered (boxes, scores and classes)
        """
        raise NotImplementedError('DeepNeuralNetwork.predict is an abstract method')
        
        
    @abstractmethod
    def show_img_with_boxes(self, title, image, boxes, scores, classes, scale=None):
        """ 
        Show image with boxes
        
        Parameters
        ----------
        image : numpy.ndarray or str
            Image path to load with OpenCV or the image itself
        boxes : list
            List of boxes to show. Boxes are in the format [x, y, width, height]
        scores : list
            List of scores for each box
        classes : list
            List of classes for each box
        """
        raise NotImplementedError('DeepNeuralNetwork.show_img_with_boxes is an abstract method')