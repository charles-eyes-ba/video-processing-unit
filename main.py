from src.domain.configs.cams import CAM_HOUSE_EXTERNAL_RIGHT, CAM_HOUSE_EXTERNAL_LEFT, CAM_HOUSE_GARAGE, CAM_HOUSE_BACKYARD
from src.domain.configs.yolo_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.domain.algorithms.personal_detection import PersonalDetection
from src.domain.algorithms.vehicle_counter import VehicleCounter

from src.external.opencv.live_video_capture import LiveVideoCapture
from src.external.opencv.yolo import YoloDNN

from src.domain.camera import Camera

import cv2


# Neural Network
yolo = YoloDNN(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)

# Setup Cams and their titles
live_video_1 = Camera(
    title="CAM_HOUSE_EXTERNAL_RIGHT",
    cam=LiveVideoCapture(CAM_HOUSE_EXTERNAL_RIGHT),
    algorithms=[VehicleCounter(), PersonalDetection()]
)

live_video_2 = Camera(
    title="CAM_HOUSE_EXTERNAL_LEFT",
    cam=LiveVideoCapture(CAM_HOUSE_EXTERNAL_LEFT),
    algorithms=[VehicleCounter()]
)

live_video_3 = Camera(
    title="CAM_HOUSE_GARAGE",
    cam=LiveVideoCapture(CAM_HOUSE_GARAGE),
    algorithms=[VehicleCounter(), PersonalDetection()]
)

live_video_4 = Camera(
    title="CAM_HOUSE_BACKYARD",
    cam=LiveVideoCapture(CAM_HOUSE_BACKYARD),
    algorithms=[VehicleCounter()]
)

live_videos = [live_video_3]

[live.start_thread(yolo) for live in live_videos]
cv2.waitKey(0)






# Main Loop
# while True:
#     for live_video in live_videos:
#         frame = live_video.cam.frame
        
#         if frame is not None and live_video.last_frame_id != frame.id:
#             live_video.last_frame_id = frame.id
            
#             title = live_video.title
#             image = frame.image
    
#             boxes, scores, classes = yolo.predict(image)
#             yolo.show_img_with_boxes(title, image, boxes, scores, classes, scale=2)
            
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
