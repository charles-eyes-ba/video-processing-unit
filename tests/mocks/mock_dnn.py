from src.external.deep_neural_network import DeepNeuralNetwork

class MockDeepNeuralNetwork(DeepNeuralNetwork):
    
    def __init__(self, config_path, weights_path, classes_path, predict=None):
        self._config_path = config_path 
        self._weights_path = weights_path 
        self._classes_path = classes_path 
        self._predict = predict
        
        self.__predict_counter = 0
    
    
    def predict(self, image):
        if self._predict is not None:
            return self._predict(image)
        else:
            counter = self.__predict_counter
            self.__predict_counter += 1
            return ([counter], [counter], [counter])
        
        
    def show_img_with_boxes(self, title, image, boxes, scores, classes, scale=None):
        pass