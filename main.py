from src.domain.configs.cams import CAM_CROSSING, CAM_STREET, CAM_EASY_STREET
from src.domain.configs.yolo_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.external.opencv.live_video_capture import LiveVideoCapture
from src.external.opencv.yolo import YoloDNN

from collections import namedtuple

import cv2

LiveVideo = namedtuple('LiveVideo', 'title cam')

yolo = YoloDNN(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)

videos = []
for cam in [CAM_CROSSING, CAM_STREET, CAM_EASY_STREET, 0]:
    videos.append(LiveVideo(str(cam), LiveVideoCapture(cam)))

while True:
    frames = [video.cam.pop_last_frame() for video in videos]
    
    for index, frame in enumerate(frames):
        if frame is not None:
            title = videos[index].title
            boxes, scores, classes = yolo.predict(frame)
            yolo.show_img_with_boxes(title, frame, boxes, scores, classes)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break