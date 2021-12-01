from threading import Thread
from time import sleep

class VideoProcessor:
    """ 
    Class that handles the video feed and the detection of the objects

    Parameters
    ----------
    id : str
        The id of the camera
    video_feed : VideoFeed
        The video feed of the camera
    dnn : DNN
        The Deep Neural Network used to detect objects
    """
    def __init__(self, id, video_feed, dnn):
        self.id = id
        self.video_feed = video_feed
        self.dnn = dnn

        self._thread = Thread(target=self._loop)
        self._thread.daemon = True
        self._thread.start()


    def _loop(self):
        """ Main loop of the video processor """
        while True:
            overview = ''
            frame = self.cam.pop_lastest_frame()

            if frame is not None:
                boxes, scores, classes = self.yolo.predict(frame)
                overview += f'Camera: {self.id} {classes}'

            print(overview)
            sleep(5)