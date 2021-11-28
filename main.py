from src.domain.configs.cams import CAM_CROSSING, CAM_STREET, CAM_EASY_STREET
from src.external.opencv.live_video_capture import LiveVideoCapture

import cv2

cams = []
for cam in [CAM_CROSSING, CAM_STREET, CAM_EASY_STREET]:
    cams.append((str(cam), LiveVideoCapture(cam)))

while True:
    frames = [cam[1].frame for cam in cams]
    
    for index, frame in enumerate(frames):
        if frame is not None:
            cv2.imshow(cams[index][0], frame)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break