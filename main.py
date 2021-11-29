from src.domain.configs.cams import CAM_CROSSING, CAM_STREET, CAM_EASY_STREET, CAM_JAPAN_ROAD
from src.domain.configs.yolo_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.external.opencv.live_video_capture import LiveVideoCapture
from src.external.opencv.yolo import YoloDNN

import cv2

yolo = YoloDNN(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)

cams = []
for cam in [CAM_CROSSING, CAM_EASY_STREET, CAM_JAPAN_ROAD]:
    cams.append((str(cam), LiveVideoCapture(cam)))

while True:
    frames = [cam[1].frame for cam in cams]
    
    for index, frame in enumerate(frames):
        if frame is not None:
            title = cams[index][0]
            boxes, scores, classes = yolo.predict(frame)
            yolo.show_img_with_boxes(title, frame, boxes, scores, classes)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break