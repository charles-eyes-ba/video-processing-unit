from src.configs.cams import CAM_HOUSE_EXTERNAL_RIGHT, CAM_HOUSE_EXTERNAL_LEFT, CAM_HOUSE_GARAGE, CAM_HOUSE_BACKYARD
from src.configs.dnn_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.video_processor import VideoProcessor
from src.opencv.video_feed import VideoFeed
from src.opencv.deep_neural_network import DeepNeuralNetwork
from src.websocket import WebSocketClient

import asyncio

class VideoProcessingUnit:
    def __init__(self):
        self._websocket = WebSocketClient('http://localhost:5000')
        self._video_feeds = [
            VideoProcessor(
                id="CAM_HOUSE_GARAGE",
                video_feed=VideoFeed(CAM_HOUSE_GARAGE),
                dnn=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH),
                websocket=self._websocket
            )
        ]


    def add_video_feed(self, video_feed):
        """ Adds a video feed to the list of video feeds to be processed """
        self._video_feeds.append(video_feed)
        
    
    def start(self):
        """ Starts all video feeds processing """
        for video_feed in self._video_feeds:
            video_feed.start()
        asyncio.get_event_loop().run_forever()