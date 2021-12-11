from src.domain.video_feed.video_feed_opencv import VideoFeedOpenCV

def create_video_feed(video_capture):
    return VideoFeedOpenCV(video_capture)