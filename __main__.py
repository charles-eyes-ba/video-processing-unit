from src.common.environment import CAM_URL
from src.factory import Factory

import cv2
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

# Components
ai_engine = Factory.ai_engine()
video_capture = Factory.video_capture(CAM_URL)

# Test
video_capture.start()
image = cv2.imread("resources/images/cam.jpg")
objs = ai_engine.extract_objects(image)

img = video_capture.pop_lastest_frame()
cv2.imwrite("resources/images/img.jpg", img)

# # Run 4ever
# asyncio.get_event_loop().run_forever()