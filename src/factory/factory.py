from src.common.environment import DEEPSTACK_URL

from src.domain.dependencies.ai_engine import AIEngine
from src.dependencies.ai_engine.deepstack_engine import DeepStackEngine

from src.domain.dependencies.video_capture import VideoCapture
from src.dependencies.video_capture.opencv_video_capture import OpenCVVideoCapture

class Factory:
    
    @staticmethod
    def ai_engine() -> AIEngine:
        return DeepStackEngine(DEEPSTACK_URL)
    
    
    @staticmethod
    def video_capture(url: str) -> VideoCapture:
        return OpenCVVideoCapture(url)