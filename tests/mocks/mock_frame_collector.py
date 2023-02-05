from src2.domain._frame_collector import FrameCollector

import numpy

class MockFrameCollector(FrameCollector):
    
    def __init__(self, video_capture, setup_callbacks=None, start=None, stop=None, pop_lastest_frame=None, release=None):
        self._video_capture = video_capture
        self._setup_callbacks = setup_callbacks
        self._start = start
        self._stop = stop
        self._pop_lastest_frame = pop_lastest_frame
        self._release = release
        
        self.started = False
        self.stopped = False
        self.released = False
        
        self.__pop_lastest_frame_counter = 0
        
        
    def setup_callbacks(self, on_error=None):
        if self._setup_callbacks is not None:
            self._setup_callbacks(on_error)
        
      
    def start(self):
        self.started = True
        if self._start is not None:
            self._start()
    
    
    def stop(self):
        self.stopped = True
        if self._stop is not None:
            self._stop()
    
    
    def pop_lastest_frame(self):
        if self._pop_lastest_frame is not None:
            return self._pop_lastest_frame()
        else:
            fake_frame = numpy.ndarray([3, 3, 3])
            fake_frame.fill(self.__pop_lastest_frame_counter)
            self.__pop_lastest_frame_counter += 1
            return fake_frame
    
    
    def release(self):
        self.released = True
        if self._release is not None:
            self._release()