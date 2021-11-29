from src.domain.configs.cams import CAM_CROSSING, CAM_STREET, CAM_EASY_STREET
from src.domain.configs.yolo_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.external.opencv.live_video_capture import LiveVideoCapture
from src.external.opencv.yolo import YoloDNN

import cv2


# Yolo Example
yolo = YoloDNN(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)
boxes, scores, classes = yolo.predict('resources/imgs/person.jpg')
yolo.show_img_with_boxes('resources/imgs/person.jpg', boxes, scores, classes)

cv2.waitKey()

# # Cams Example
# def cam_example():
#     cams = []
#     for cam in [CAM_CROSSING, CAM_STREET, CAM_EASY_STREET]:
#         cams.append((str(cam), LiveVideoCapture(cam)))

#     while True:
#         frames = [cam[1].frame for cam in cams]
        
#         for index, frame in enumerate(frames):
#             if frame is not None:
#                 cv2.imshow(cams[index][0], frame)
                
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break