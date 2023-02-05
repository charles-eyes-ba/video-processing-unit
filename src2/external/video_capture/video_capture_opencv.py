from src2.domain._video_capture import VideoCapture
from .exceptions import VideoCaptureCouldNotConnect, VideoCaptureConnectionLost

import cv2

class VideoCaptureOpenCV(VideoCapture):
    def __init__(self, url):
        self.__url = url
        self._cap = cv2.VideoCapture(self.__url)
        if self._cap is None or not self._cap.isOpened():
            raise VideoCaptureCouldNotConnect(f'Could not connect to video source: {self.__url}')
        self._cap.setExceptionMode(True)
    
        
    def read(self):
        try:
            _, frame = self._cap.read()
        except:
            raise VideoCaptureConnectionLost(f'Connection to video source lost: {self.__url}')
        return frame
    
    
    def release(self):
        self._cap.release()