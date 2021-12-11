from .interface import VideoCapture

import cv2

class VideoCaptureOpenCV(VideoCapture):
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)
        
    def read(self):
        _, frame = self.cap.read()
        return frame