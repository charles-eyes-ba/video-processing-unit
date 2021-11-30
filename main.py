from src.domain.configs.cams import CAM_HOUSE_EXTERNAL_RIGHT, CAM_HOUSE_EXTERNAL_LEFT, CAM_HOUSE_GARAGE, CAM_HOUSE_BACKYARD
from src.domain.configs.yolo_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.domain.algorithms.vehicle_counter import VehicleCounter
from src.domain.algorithms.personal_detection import PersonalDetection

from src.external.opencv.live_video_capture import LiveVideoCapture
from src.external.opencv.yolo import YoloDNN

from time import sleep
from threading import Thread

import cv2

# Aux Struct
class LiveVideo:
    def __init__(self, title, cam, algorithms):
        self.title = title
        self.cam = cam
        self.last_frame_id = None
        self.algorithms = algorithms
        
    
    def _loop(self, yolo, delay=1):
        while True:
            frame = self.cam.frame
            
            if frame is not None and self.last_frame_id != frame.id:
                self.last_frame_id = frame.id
                boxes, scores, classes = yolo.predict(frame.image)
                
                for algorithm in self.algorithms:
                    if type(algorithm) is VehicleCounter:
                        vehicles_len = algorithm.run(boxes, scores, classes)
                        print(self.title, vehicles_len)
                    elif type(algorithm) is PersonalDetection:
                        personal = algorithm.run(boxes, scores, classes)
                        print(self.title, personal)

            sleep(delay)
        
        
    def start_thread(self, yolo, delay=1):
        thread = Thread(target=self._loop, args=(yolo, delay))
        thread.start()
        


# Neural Network
yolo = YoloDNN(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)


# Setup Cams and their titles
live_video_1 = LiveVideo(
    title="CAM_HOUSE_EXTERNAL_RIGHT",
    cam=LiveVideoCapture(CAM_HOUSE_EXTERNAL_RIGHT),
    algorithms=[VehicleCounter(), PersonalDetection()]
)

live_video_2 = LiveVideo(
    title="CAM_HOUSE_EXTERNAL_LEFT",
    cam=LiveVideoCapture(CAM_HOUSE_EXTERNAL_LEFT),
    algorithms=[VehicleCounter()]
)

live_video_3 = LiveVideo(
    title="CAM_HOUSE_GARAGE",
    cam=LiveVideoCapture(CAM_HOUSE_GARAGE),
    algorithms=[VehicleCounter(), PersonalDetection()]
)

live_video_4 = LiveVideo(
    title="CAM_HOUSE_BACKYARD",
    cam=LiveVideoCapture(CAM_HOUSE_BACKYARD),
    algorithms=[VehicleCounter()]
)

live_videos = [live_video_3, live_video_4]

[live.start_thread(yolo) for live in live_videos]
cv2.waitKey(0)

# # Main Loop
# while True:
#     for live_video in live_videos:
#         frame = live_video.cam.frame
        
#         if frame is not None and live_video.last_frame_id != frame.id:
#             live_video.last_frame_id = frame.id
            
#             title = live_video.title
#             image = frame.image
    
#             boxes, scores, classes = yolo.predict(image)
            
#             for alg in live_video.algorithms:
#                 if type(alg) is VehicleCounter:
#                     vehicles_len = alg.run(boxes, scores, classes)
#                     print(vehicles_len)
#                 elif type(alg) is PersonalDetection:
#                     personal = alg.run(boxes, scores, classes)
#                     print(personal)
            
#             yolo.show_img_with_boxes(title, image, boxes, scores, classes, scale=2)
            
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
