from threading import Thread
from time import sleep

class Camera:
    """ Class that contains the camera and its algorithms """
    def __init__(self, id, cam, yolo):
        self.id = id
        self.cam = cam
        self.yolo = yolo


    def pop_lastest_frame(self):
        """ Returns the lastest frame from the camera """
        return self.cam.pop_lastest_frame()


    def start_thread(self):
        """ Starts the thread """
        thread = Thread(target=self._lopp)
        thread.daemon = True
        thread.start()


    def _lopp(self):
        """ Loops the camera """
        while True:
            overview = ''
            frame = self.cam.pop_lastest_frame()

            if frame is not None:
                boxes, scores, classes = self.yolo.predict(frame)
                overview += f'Camera: {self.id} {classes}'

            print(overview)
            sleep(5)