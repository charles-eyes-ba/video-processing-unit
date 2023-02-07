import logging
from src.common.logger import logger

from src.common.environment import WEBSOCKET_URL
from src.common.environment import CAM_JARDIM_URL, CAM_QUINTAL_URL, CAM_RUA_DIREITA_URL, CAM_RUA_ESQUERDA_URL

from src.domain.components.main_unit import MainUnit, MainUnitWebSocket
from src.integration.websocket.socketio import WebSocketIO


logger.setLevel(level=logging.DEBUG)
logger.debug('Starting __main__')

# websocket = WebSocketIO(WEBSOCKET_URL)
# vpu = MainUnitWebSocket(websocket)
# vpu.start()

websocket = WebSocketIO(WEBSOCKET_URL)
websocket.connect()