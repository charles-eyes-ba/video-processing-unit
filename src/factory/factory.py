from src.common.environment import DEEPSTACK_URL

from src.domain.dependencies.ai_engine import AIEngine
from src.dependencies.ai_engine.deepstack_engine import DeepStackEngine

class Factory:
    
    @staticmethod
    def ai_engine() -> AIEngine:
        return DeepStackEngine(DEEPSTACK_URL)