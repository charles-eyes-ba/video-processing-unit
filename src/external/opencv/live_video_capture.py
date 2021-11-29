from threading import Thread

import cv2

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
            self.status, self.frame = self._cam.read()