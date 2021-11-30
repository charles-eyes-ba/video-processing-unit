from src.domain.configs.cams import CAM_HOUSE_EXTERNAL_RIGHT, CAM_HOUSE_EXTERNAL_LEFT, CAM_HOUSE_GARAGE, CAM_HOUSE_BACKYARD
from src.domain.configs.yolo_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.external.opencv.live_video_capture import LiveVideoCapture
from src.external.opencv.yolo import YoloDNN

from src.domain.camera import Camera

import cv2


# Neural Network
yolo = YoloDNN(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)


# # Setup Cams and their titles
# camera_1 = Camera(
#     id="CAM_HOUSE_EXTERNAL_RIGHT",
#     cam=LiveVideoCapture(CAM_HOUSE_EXTERNAL_RIGHT)
# )

# camera_2 = Camera(
#     id="CAM_HOUSE_EXTERNAL_LEFT",
#     cam=LiveVideoCapture(CAM_HOUSE_EXTERNAL_LEFT)
# )

# camera_3 = Camera(
#     id="CAM_HOUSE_GARAGE",
#     cam=LiveVideoCapture(CAM_HOUSE_GARAGE)
# )

# camera_4 = Camera(
#     id="CAM_HOUSE_BACKYARD",
#     cam=LiveVideoCapture(CAM_HOUSE_BACKYARD)
# )

# for camera in [camera_3]:
#     camera.start_thread(yolo)

cv2.waitKey(0)