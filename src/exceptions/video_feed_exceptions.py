class VideoFeedCouldNotConntect(Exception):
    def __init__(self, message):
        self.message = message

class VideoFeedConnectionLost(Exception):
    def __init__(self, message):
        self.message = message