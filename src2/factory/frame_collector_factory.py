from src2.domain.frame_collector.frame_collector_impl import FrameCollectorImpl

def create_frame_collector(video_capture):
    return FrameCollectorImpl(video_capture)