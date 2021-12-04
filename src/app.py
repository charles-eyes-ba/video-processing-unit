class VideoProcessingUnit:
    def __init__(self):
        self._video_feeds = []

    def start_all(self):
        for video_feed in self._video_feeds:
            video_feed.start()