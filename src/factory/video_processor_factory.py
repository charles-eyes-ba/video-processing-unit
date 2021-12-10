from src.domain.video_processor.video_processor_impl import VideoProcessorImpl

def create_video_processor(id, video_feed, dnn, delay=5):
    return VideoProcessorImpl(id, video_feed, dnn, delay)