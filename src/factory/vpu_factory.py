from src.domain.video_processing_unit import VideoProcessingUnit

def create_vpu(websocket, create_detector):
    return VideoProcessingUnit(websocket, create_detector)