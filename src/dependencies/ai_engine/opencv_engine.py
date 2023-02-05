import cv2
import numpy

from src.domain.dependencies.ai_engine import AIEngine
from .exceptions import InvalidDNNFilesException

class OpenCVEngine(AIEngine):
    def __init__(self, config_path, weights_path, classes_path):
        self._threshold = 0.55
        self._threshold_NMS = 0.3
        self._blob_size = (416, 416)

        try: 
            self._net = cv2.dnn.readNet(config_path, weights_path)
            self._classes = open(classes_path).read().strip().split('\n')
        except Exception as e:
            raise InvalidDNNFilesException('Invalid deep neural network files')
        
        
    def extract_objects(self, image: numpy.ndarray) -> list[str]:
        image = self._read_image(image) if type(image) == str else image
        height, width = image.shape[:2]
        output_results = self._predict_boxes(image)
        _, _, filtered_classes = self._filter_boxes(output_results, width, height)
        return filtered_classes
    
    
    def _read_image(self, image_path):
        """ 
        Read image from path
        
        Parameters
        ----------
        image_path : str
            Image path to load with OpenCV
            
        Returns
        -------
        numpy.ndarray
            Image loaded with OpenCV
        """
        return cv2.imread(image_path)
    
    
    def _predict_boxes(self, image):
        """ 
        Predict bounding boxes 
        
        Parameters
        ----------
        image : numpy.ndarray
            OpenCV image to predict detections with DNN
            
        Returns
        -------
        tuple
            Tuple with all detections predicted by DNN
        """
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, self._blob_size, swapRB=True, crop=False)
        self._net.setInput(blob)
        return self._net.forward(self._output_layers)
    
    
    def _filter_boxes(self, output_results, width, height):
        """ 
        Filter boxes with threshold and apply non maximum suppression
        
        Parameters
        ----------
        output_results : opencv image or str
            All detections prediteced by Yolo
        width : double 
            Width to rescale the boxes
        height : double
            Height to rescale the boxes
            
        Returns
        -------
        tuple
            Tuple with all detections filtered (boxes, scores and classes)
        """
        boxes = []
        scores = []
        classes_ids = []

        for output_layer in output_results:
            for detection in output_layer:
                classes_scores = detection[5:]
                class_index = numpy.argmax(classes_scores)
                
                max_score = classes_scores[class_index]
                if max_score > self._threshold:
                    box = detection[0:4] * numpy.array([width, height, width, height])
                    (box_center_x, box_center_y , box_width, box_height) = box.astype('int')

                    x = int(box_center_x - box_width / 2)
                    y = int(box_center_y - box_height / 2)

                    boxes.append([x, y, int(box_width), int(box_height)])
                    scores.append(float(max_score))
                    classes_ids.append(class_index)
             
        indexes = cv2.dnn.NMSBoxes(boxes, scores, self._threshold, self._threshold_NMS)
        
        filtered_boxes, filtered_scores, filtered_classes = [], [], []
        for index in indexes:
            filtered_boxes.append(boxes[index])
            filtered_scores.append(scores[index])
            filtered_classes.append(self._classes[classes_ids[index]])
            
        return filtered_boxes, filtered_scores, filtered_classes