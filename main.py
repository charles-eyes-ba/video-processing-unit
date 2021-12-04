from src.configs.cams import CAM_HOUSE_EXTERNAL_RIGHT, CAM_HOUSE_EXTERNAL_LEFT, CAM_HOUSE_GARAGE, CAM_HOUSE_BACKYARD
from src.configs.dnn_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.opencv.video_feed import VideoFeed
from src.opencv.deep_neural_network import DeepNeuralNetwork

from src.video_processor import VideoProcessor
from src.websocket import WebSocketClient

import asyncio

websocket = WebSocketClient(url='http://localhost:5000/')

# Setup Video Processors
# camera_1 = VideoProcessor(
#     id="CAM_HOUSE_EXTERNAL_RIGHT",
#     video_feed=VideoFeed(CAM_HOUSE_EXTERNAL_RIGHT),
#     dnn=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH),
#     websocket=websocket
# )

# camera_2 = VideoProcessor(
#     id="CAM_HOUSE_EXTERNAL_LEFT",
#     video_feed=VideoFeed(CAM_HOUSE_EXTERNAL_LEFT),
#     dnn=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH),
#     websocket=websocket
# )

camera_3 = VideoProcessor(
    id="CAM_HOUSE_GARAGE",
    video_feed=VideoFeed(CAM_HOUSE_GARAGE),
    dnn=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH),
    websocket=websocket
)

# camera_4 = VideoProcessor(
#     id="CAM_HOUSE_BACKYARD",
#     video_feed=VideoFeed(CAM_HOUSE_BACKYARD),
#     dnn=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH),
#     websocket=websocket
# )

# camera_5 = VideoProcessor(
#     id="CAM_HOUSE_BACKYARD_5",
#     video_feed=VideoFeed(CAM_HOUSE_BACKYARD),
#     dnn=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH),
#     websocket=websocket
# )

# camera_6 = VideoProcessor(
#     id="CAM_HOUSE_BACKYARD_6",
#     video_feed=VideoFeed(CAM_HOUSE_BACKYARD),
#     dnn=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH),
#     websocket=websocket
# )

# camera_7 = VideoProcessor(
#     id="CAM_HOUSE_BACKYARD_7",
#     video_feed=VideoFeed(CAM_HOUSE_BACKYARD),
#     dnn=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH),
#     websocket=websocket
# )

# camera_8 = VideoProcessor(
#     id="CAM_HOUSE_BACKYARD_8",
#     video_feed=VideoFeed(CAM_HOUSE_BACKYARD),
#     dnn=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH),
#     websocket=websocket
# )

asyncio.get_event_loop().run_forever()