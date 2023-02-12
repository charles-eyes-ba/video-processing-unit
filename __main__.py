import logging
from src.common.logger import logger

from src.domain.components.main_unit import MainUnitWebSocket
from src.dependency_injector.dependency_injector import DependencyInjector
from src.models.video_feed import VideoFeed


logger.setLevel(level=logging.DEBUG)
logger.debug('Starting __main__')

dependencies = DependencyInjector()
vpu = MainUnitWebSocket(dependencies)
vpu.start()