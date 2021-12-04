from src.configs.dnn_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.video_processor import VideoProcessor
from src.opencv.video_feed import VideoFeed
from src.opencv.deep_neural_network import DeepNeuralNetwork
from src.websocket import WebSocketClient

import asyncio

class VideoProcessingUnit:
    
    def __init__(self):
        self._websocket = WebSocketClient('http://localhost:5000')
        self.setup_websocket_callbacks()
        self._video_feeds = []


    # * Setups | Generates
    def generate_deep_neural_network(self):
        """ Generates a deep neural network """
        return DeepNeuralNetwork(
            config_path=YOLO_CONFIG_PATH, 
            weights_path=YOLO_WEIGHTS_PATH, 
            classes_path=YOLO_CLASSES_PATH
        )


    def setup_websocket_callbacks(self):
        """ Sets up the websocket client """
        self._websocket.on_video_feeds_update = self.update_video_feed_list


    # * Handle videos feed list
    def update_video_feed_list(self, video_feed_list):
        """ Updates the list of video feeds to be processed """
        self._video_feeds = []
        for video_feed in video_feed_list:
            processor = VideoProcessor(
                id=video_feed['id'],
                video_feed=VideoFeed(video_feed['feed_url']),
                dnn=self.generate_deep_neural_network(),
                websocket=self._websocket
            )
            self._video_feeds.append(processor)
        self._start_video_processors()


    def add_video_feed(self, video_feed):
        """ Adds a video feed to the list of video feeds to be processed """
        self._video_feeds.append(VideoProcessor(
            id=video_feed['id'],
            video_feed=VideoFeed(video_feed['feed_url']),
            dnn=self.generate_deep_neural_network(),
            websocket=self._websocket
        ))
        
        
    def remove_vide_feed(self, video_feed_id):
        """ Removes a video feed from the list of video feeds to be processed """
        for video in self._video_feeds:
            if video.id == video_feed_id:
                self._video_feeds.remove(video)
                break
    
    
    # * Starts
    def _start_video_processors(self):
        """ Starts all video feeds processing """
        for video_feed in self._video_feeds:
            video_feed.start()
    
    
    def start(self):
        """ Starts video processing unit aplication """
        self._start_video_processors()
        asyncio.get_event_loop().run_forever()