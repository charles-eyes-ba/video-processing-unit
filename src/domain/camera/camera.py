from src.domain.algorithms.personal_detection import PersonalDetection
from src.domain.algorithms.vehicle_counter import VehicleCounter

from threading import Thread
from time import sleep

class Camera:
    """ Class that contains the camera and its algorithms """
    def __init__(self, title, cam, algorithms):
        self.title = title
        self.cam = cam
        self.last_frame_id = None
        self.algorithms = algorithms
        
    
    def _loop(self, yolo, delay=1):
        """ Loop that runs the camera and its algorithms with a delay """
        while True:
            frame = self.cam.frame
            
            if frame is not None and self.last_frame_id != frame.id:
                self.last_frame_id = frame.id
                boxes, scores, classes = yolo.predict(frame.image)
                
                for algorithm in self.algorithms:
                    if type(algorithm) is VehicleCounter:
                        vehicles_len = algorithm.run(boxes, scores, classes)
                        print(self.title, vehicles_len)
                    elif type(algorithm) is PersonalDetection:
                        personal = algorithm.run(boxes, scores, classes)
                        print(self.title, personal)

            sleep(delay)
        
        
    def start_thread(self, yolo, delay=1):
        """ Starts the camera loop in a new thread """
        thread = Thread(target=self._loop, args=(yolo, delay))
        thread.start()