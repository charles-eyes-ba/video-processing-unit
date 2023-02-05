from src2.domain._video_capture import VideoCapture

class MockVideoCapture(VideoCapture):
    
    def __init__(self, url, read=None, release=None):
        self.url = url
        self._read = read
        self._release = release
        self.released = False
        
        
    def read(self):
        if self._read is not None:
            return self._read()
            
            
    def release(self):
        self.released = True
        if self._release is not None:
            self._release()