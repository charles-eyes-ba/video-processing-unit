from src.domain.configs.cams import CAM_CROSSING, CAM_STREET, CAM_EASY_STREET, CAM_PEOPLE, CAM_GARAGE
from src.domain.configs.cams import CAM_HOUSE_EXTERNAL_RIGHT, CAM_HOUSE_EXTERNAL_LEFT, CAM_HOUSE_GARAGE, CAM_HOUSE_BACKYARD
from src.domain.configs.yolo_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.external.opencv.live_video_capture import LiveVideoCapture
from src.external.opencv.yolo import YoloDNN

from collections import namedtuple

import cv2

# Aux Struct
LiveVideo = namedtuple('LiveVideo', 'title cam')

# Neural Network
yolo = YoloDNN(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)

# Setup Cams and their titles
videos = []
for cam in [CAM_HOUSE_GARAGE, CAM_HOUSE_BACKYARD]:
    videos.append(LiveVideo(str(cam), LiveVideoCapture(cam)))
    
# Main Loop
while True:
    # Get last frame from each cam
    frames = [video.cam.pop_last_frame() for video in videos]
    
    for index, frame in enumerate(frames):
        if frame is not None:
            title = videos[index].title
            frame = cv2.resize(frame, dsize=None,fx=2,fy=2)

            boxes, scores, classes = yolo.predict(frame)
            yolo.show_img_with_boxes(title, frame, boxes, scores, classes)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
