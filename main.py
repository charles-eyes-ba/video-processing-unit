from src.domain.configs.cams import CAM_HOUSE_EXTERNAL_RIGHT, CAM_HOUSE_EXTERNAL_LEFT, CAM_HOUSE_GARAGE, CAM_HOUSE_BACKYARD
from src.domain.configs.yolo_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.external.opencv.live_video_capture import LiveVideoCapture
from src.external.opencv.yolo import YoloDNN

from src.domain.camera import Camera
from datetime import datetime

import cv2

# Neural Network
yolo = YoloDNN(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)


# Setup Cams and their titles
camera_1 = Camera(
    id="CAM_HOUSE_EXTERNAL_RIGHT",
    cam=LiveVideoCapture(CAM_HOUSE_EXTERNAL_RIGHT)
)

camera_2 = Camera(
    id="CAM_HOUSE_EXTERNAL_LEFT",
    cam=LiveVideoCapture(CAM_HOUSE_EXTERNAL_LEFT)
)

camera_3 = Camera(
    id="CAM_HOUSE_GARAGE",
    cam=LiveVideoCapture(CAM_HOUSE_GARAGE)
)

camera_4 = Camera(
    id="CAM_HOUSE_BACKYARD",
    cam=LiveVideoCapture(CAM_HOUSE_BACKYARD)
)


# Loop
while True:
    overview = ''
    start_time = datetime.now()

    for camera in [camera_1, camera_2, camera_3, camera_4]:
        frame = camera.pop_lastest_frame()

        if frame is not None:
            boxes, scores, classes = yolo.predict(frame)
            overview += f'Camera: {camera.id} {classes}\n'

    overview += f'Time to process: {datetime.now() - start_time}\n'
    overview += f'Stated time: {start_time}\n'
    print(overview)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
