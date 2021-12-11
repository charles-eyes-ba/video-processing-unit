from src.domain.detector.detector_impl import DetectorImpl

def create_detector(id, video_capture, dnn, delay=5):
    return DetectorImpl(id, video_capture, dnn, delay)