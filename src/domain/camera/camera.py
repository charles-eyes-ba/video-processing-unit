from threading import Thread
from time import sleep

class Camera:
    """ Class that contains the camera and its algorithms """
    def __init__(self, id, cam):
        self.id = id
        self.cam = cam
        self.last_frame_id = None
        
    
    def _loop(self, yolo, delay=1):
        """ Loop that runs the camera and its algorithms with a delay """
        print(f'started {self.id}')
        while True:
            frame = self.cam.frame
            
            if frame is not None and frame.image is not None and self.last_frame_id != frame.id:
                self.last_frame_id = frame.id
                boxes, scores, classes = yolo.predict(frame.image)
                print(f'{self.id}: {len(boxes)}')

            sleep(delay)
        
        
    def start_thread(self, yolo, delay=1):
        """ Starts the camera loop in a new thread """
        thread = Thread(target=self._loop, args=(yolo, delay))
        thread.start()