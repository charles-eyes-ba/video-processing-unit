import logging
from src.common.logger import logger

from src.domain.components.main_unit import MainUnitWebSocket
from src.dependency_injector import DependencyInjector


logger.setLevel(level=logging.DEBUG)
logger.debug('Starting __main__')

dependencies = DependencyInjector()
vpu = MainUnitWebSocket(dependencies)
vpu.start()