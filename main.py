from src.domain.configs.cams import CAM_CROSSING
from src.external.opencv.live_video_capture import LiveVideoCapture

import cv2

cam = LiveVideoCapture(0, lambda _, frame: cv2.imshow('frame', frame))

while True:
    frame = cam.frame
    if frame is not None:
        mirror = cv2.flip(frame, 1)
        cv2.imshow('frame', mirror)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break