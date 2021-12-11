from src.external.deep_neural_network import DeepNeuralNetwork

class MockDeepNeuralNetwork(DeepNeuralNetwork):
    
    def __init__(self, config_path, weights_path, classes_path, __init__=None, predict=None):
        self._config_path = config_path 
        self._weights_path = weights_path 
        self._classes_path = classes_path 
        self._init_ = __init__
        self._predict = predict
    
    
    def predict(self, image):
        if self._predict is not None:
            return self._predict(image)