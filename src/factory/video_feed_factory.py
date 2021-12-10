from src.video_feed.video_feed_opencv import VideoFeedOpenCV

def create_video_feed(feed_url):
    return VideoFeedOpenCV(feed_url)