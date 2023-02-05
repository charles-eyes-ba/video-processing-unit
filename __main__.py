from src.common.environment import CAM_URL
from src.factory import Factory

import cv2
import time
import logging

logging.basicConfig(level=logging.INFO)

# Components
ai_engine = Factory.ai_engine()
video_capture = Factory.video_capture(CAM_URL)

video_capture.start()

# Test
time.sleep(2)

image = video_capture.pop_lastest_frame()
cv2.imwrite("resources/images/img_1.jpg", image)

objs = ai_engine.extract_objects(image)