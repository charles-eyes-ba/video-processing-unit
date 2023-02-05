from numpy import ndarray
from deepstack_sdk import ServerConfig, Detection
from src.domain.dependencies.ai_engine import AIEngine

import logging

class DeepStackEngine(AIEngine):
    def __init__(self, deepstack_url: str, threshold: float = 0.5):
        self._threshold = threshold
        self._deepstack_url = deepstack_url
        self._deepstack_config = ServerConfig(deepstack_url)
        self._detection = Detection(self._deepstack_config)
        logging.info(':DeepStackEngine: initialized')
        
        
    def extract_objects(self, image: ndarray) -> list[str]:
        objects = []
        for obj in self._detection.detectObject(image):
            if obj.confidence >= self._threshold:
                objects.append(obj.label)
        logging.info(f':DeepStackEngine: objects found {objects}')
        return objects