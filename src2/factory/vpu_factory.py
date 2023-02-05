from src2.domain.video_processing_unit.video_processing_unit_impl import VideoProcessingUnitImpl

def create_vpu(websocket, create_detector):
    return VideoProcessingUnitImpl(websocket, create_detector)