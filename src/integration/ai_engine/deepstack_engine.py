import base64
from numpy import ndarray
from deepstack_sdk import ServerConfig, Detection, Enhance
from src.domain.dependencies.ai_engine import AIEngine

import logging

class DeepStackEngine(AIEngine):
    def __init__(self, deepstack_url: str, threshold: float = 0.5):
        self._threshold = threshold
        self._deepstack_url = deepstack_url
        self._deepstack_config = ServerConfig(deepstack_url)
        self._detection = Detection(self._deepstack_config)
        self._enhancer = Enhance(self._deepstack_config)
        logging.info(':DeepStackEngine: initialized')
        
        
    def extract_objects(self, image: ndarray) -> list[str]:
        objects = []
        
        image_enhanced = self._enhancer.enhanceObject(image)
        image4X_byte = base64.b64decode(image_enhanced.base64)
        
        for obj in self._detection.detectObject(image4X_byte):
            if obj.confidence >= self._threshold:
                objects.append(obj.label)
                
        logging.info(f':DeepStackEngine: objects found {objects}')
        return objects