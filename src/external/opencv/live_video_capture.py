from threading import Thread
from copy import deepcopy
from datetime import datetime

import cv2

class Frame:
    """ Frame image with id """
    def __init__(self, image, datetime):
        self.id = datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        self.image = image

class LiveVideoCapture:
    """
    Class that wraps a video capture object and provides a lastest frame
    
    Parameters
    ----------
    cam : str or int
        URL (str) or code (int) to access remote video or local camera
    """
    def __init__(self, cam):
        self.status = None
        self.frame = None
        
        self._cam = cv2.VideoCapture(cam)
        
        self.width = int(self._cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self._cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self._cam.get(cv2.CAP_PROP_FPS))
        
        self._thread = Thread(target=self._update, args=())
        self._thread.daemon = True
        self._thread.start()
        
        
    def release(self):
        """ Release the video capture object """
        self._cam.release()


    def _update(self):
        """ Update the lastest frame """
        while True:
            self.status, frame = self._cam.read()
            self.frame = Frame(frame, datetime.now())