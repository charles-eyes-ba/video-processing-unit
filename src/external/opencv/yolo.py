import cv2
import numpy

class YoloDNN:
    """
    Class that wraps a video capture object and provides a lastest frame
    
    Parameters
    ----------
    config_path : str
        Path to load Yolo config file
    weights_path : str
        Path to load Yolo weights file
    classes_path : str
        Path to load Yolo classes names file
    """
    def __init__(self, config_path, weights_path, classes_path):
        self._threshold = 0.5
        self._threshold_NMS = 0.3
        self._blob_size = (416, 416)

        self._net = cv2.dnn.readNet(config_path, weights_path)
        
        self._classes = open(classes_path).read().strip().split('\n')
        self._classes_colors = self._get_classes_colors()
        
        self._output_layers = self._get_output_layers()
        
        
    def _get_classes_colors(self):
        """ Get classes box colors """
        colors = {}
        numpy.random.seed(42)
        for class_name in self._classes:
            colors[class_name] = numpy.random.randint(0, 255, 3)
        return colors
        
        
    def _get_output_layers(self):
        """ Get output layers in Yolo architecture """
        layers = self._net.getLayerNames()
        output_layers_indexs = self._net.getUnconnectedOutLayers()
        return [layers[i - 1] for i in output_layers_indexs]
    
    
    def _read_image(self, image_path):
        """ 
        Read image from path
        
        Parameters
        ----------
        image_path : str
            Image path to load with OpenCV
        """
        return cv2.imread(image_path)
    
    
    def _predict_boxes(self, image):
        """ 
        Predict bounding boxes 
        
        Parameters
        ----------
        image : opencv image
            OpenCV image to predict detections with Yolo
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
    
    
    def predict(self, image):
        """ 
        Predict objects in image 
        
        Parameters
        ----------
        image : opencv image or str
            Image path to load with OpenCV or the image itself
        """
        image = self._read_image(image) if type(image) == str else image
        height, width = image.shape[:2]
        output_results = self._predict_boxes(image)
        return self._filter_boxes(output_results, width, height)
        
        
    def show_img_with_boxes(self, image, boxes, scores, classes):
        """ 
        Show image with boxes
        
        Parameters
        ----------
        image : opencv image or str
            Image path to load with OpenCV or the image itself
        boxes : list
            List of boxes to show. Boxes are in the format [x, y, width, height]
        scores : list
            List of scores for each box
        classes : list
            List of classes for each box
        """
        THICKESS = 2
        
        image = self._read_image(image) if type(image) == str else image
        for index, _ in enumerate(boxes):
            (x, y, width, height) = boxes[index]
            
            class_name = classes[index]
            score = scores[index]
            color = [int(c) for c in self._classes_colors[class_name]]
            text = f'{class_name}: {score:.2f}'

            background_box = numpy.full((image.shape), (0,0,0), dtype=numpy.uint8)
            cv2.putText(background_box, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), THICKESS)
            
            bx, by, bw, bh = cv2.boundingRect(background_box[:,:,2])
            cv2.rectangle(image, (x,y), (x+width, y+height), color, THICKESS)
            cv2.rectangle(image, (bx,by), (bx+bw, by+bh), color, -1)
            cv2.rectangle(image, (bx,by), (bx+bw, by+bh), color, 3)
            cv2.putText(image, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
            
        cv2.imshow('Yolo', image)