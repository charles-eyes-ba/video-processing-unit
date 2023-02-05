from src.common.environment import CAM_URL
from src.factory import Factory

import asyncio
import logging

logging.basicConfig(level=logging.INFO)

# Components
ai_engine = Factory.ai_engine()
video_capture = Factory.video_capture(CAM_URL)
video_detector = Factory.video_detector(CAM_URL, video_capture, ai_engine)

video_detector.setup_callbacks(
    on_object_detection=lambda id, objects: print(id, objects),
    on_error=lambda error: print(error)
)
video_detector.start()

# Run 4Ever
asyncio.get_event_loop().run_forever()