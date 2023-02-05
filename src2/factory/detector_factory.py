from src2.domain.detector.detector_impl import DetectorImpl

def create_detector(id, frame_collector, dnn, delay=5):
    return DetectorImpl(id, frame_collector, dnn, delay)