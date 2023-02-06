from dotenv import load_dotenv
import os

load_dotenv()

DEEPSTACK_URL = os.getenv('DEEPSTACK_URL')
WEBSOCKET_URL = os.getenv('WEBSOCKET_URL')
CAM_JARDIM_URL = 'rtsp://888888:888888@192.168.68.116:554/cam/realmonitor?channel=3'
CAM_QUINTAL_URL = 'rtsp://888888:888888@192.168.68.116:554/cam/realmonitor?channel=4'
CAM_RUA_ESQUERDA_URL = 'rtsp://888888:888888@192.168.68.116:554/cam/realmonitor?channel=1'
CAM_RUA_DIREITA_URL = 'rtsp://888888:888888@192.168.68.116:554/cam/realmonitor?channel=2'