from .interface import VideoCapture
from .exceptions import VideoCaptureCouldNotConnect, VideoCaptureConnectionLost

import cv2

class VideoCaptureOpenCV(VideoCapture):
    def __init__(self, path):
        self.__path = path
        self._cap = cv2.VideoCapture(self.__path)
        if self._cap is None or not self._cap.isOpened():
            raise VideoCaptureCouldNotConnect(f'Could not connect to video source: {self.__path}')
        self._cap.setExceptionMode(True)
        
    def read(self):
        try:
            _, frame = self._cap.read()
        except:
            raise VideoCaptureConnectionLost(f'Connection to video source lost: {self.__path}')
        return frame