from src.external.video_capture import VideoCapture

class MockVideoCapture(VideoCapture):
    
    def __init__(self, url, read=None, release=None):
        self.released = False
        self._read = read
        self._release = release
        
        
    def read(self):
        if self._read is not None:
            return self._read()
            
            
    def release(self):
        self.released = True
        if self._release is not None:
            self._release()