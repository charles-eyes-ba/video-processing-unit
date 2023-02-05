from src.factory import Factory
import cv2

import logging
logging.basicConfig(level=logging.INFO)

image = cv2.imread("resources/images/cam.jpg")
ai_engine = Factory.ai_engine()
objs = ai_engine.extract_objects(image)