import logging
from src.common.logger import logger

from src.common.environment import WEBSOCKET_URL
from src.common.environment import CAM_JARDIM_URL, CAM_QUINTAL_URL, CAM_RUA_DIREITA_URL, CAM_RUA_ESQUERDA_URL

from src.domain.components.main_unit import MainUnit, MainUnitWebSocket
from src.integration.websocket.socketio import WebSocketIO


logger.setLevel(level=logging.DEBUG)
logger.debug('Starting __main__')

websocket = WebSocketIO(WEBSOCKET_URL)
vpu = MainUnitWebSocket(websocket)

vpu.start()









# # Video Feed
# class VideoFeed:
#     def __init__(self, url, id):
#         self.url = url
#         self.id = id

# # Components
# vpu = MainUnit()
# vpu.update_video_feed_list([
#     VideoFeed(
#         url=CAM_JARDIM_URL,
#         id="camera_jardim"
#     ),
#     VideoFeed(
#         url=CAM_QUINTAL_URL,
#         id="camera_quintal"
#     ),
#     VideoFeed(
#         url=CAM_RUA_DIREITA_URL,
#         id="camera_rua_direita"
#     ),
#     VideoFeed(
#         url=CAM_RUA_ESQUERDA_URL,
#         id="camera_rua_esquerda"
#     )
# ])