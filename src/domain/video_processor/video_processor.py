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
    def __init__(self, id, video_feed, dnn, delay=5):
        self.id = id
        self._video_feed = video_feed
        self._dnn = dnn
        self._delay = delay

        self._thread = Thread(target=self._loop)
        self._thread.daemon = True
        self._thread.start()


    def _loop(self):
        """ Main loop of the video processor """
        while True:
            overview = ''
            frame = self._video_feed.pop_lastest_frame()

            if frame is not None:
                boxes, scores, classes = self._dnn.predict(frame)
                overview += f'Video Processor: {self.id} {classes}'

            print(overview)
            sleep(self._delay)