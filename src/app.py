from src import video_processor
from src.configs.dnn_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.video_processor import VideoProcessor
from src.opencv.video_feed import VideoFeed
from src.opencv.deep_neural_network import DeepNeuralNetwork
from src.websocket import WebSocketClient

import asyncio

class VideoProcessingUnit:
    """ 
    Class that handles the video processing unit 
    
    Methods
    -------
    start()
        Starts the video processing unit
    """
    def __init__(self):
        self._websocket = WebSocketClient('http://192.168.68.135:5000')
        self._setup_websocket_callbacks()
        self._video_feeds = []


    # * Setups | Generates
    def _generate_deep_neural_network(self):
        """ Generates a deep neural network """
        return DeepNeuralNetwork(
            config_path=YOLO_CONFIG_PATH, 
            weights_path=YOLO_WEIGHTS_PATH, 
            classes_path=YOLO_CLASSES_PATH
        )


    def _setup_websocket_callbacks(self):
        """ Sets up the websocket client """
        self._websocket.on_video_feeds_update = self._update_video_feed_list
        self._websocket.on_add_video_feed = self._add_video_feed
        self._websocket.on_remove_video_feed = self._remove_vide_feed


    # * Handle videos feed list
    def _update_video_feed_list(self, video_feed_list):
        """ Updates the list of video feeds to be processed """
        self._video_feeds = []
        for video_feed in video_feed_list:
            processor = VideoProcessor(
                id=video_feed['id'],
                video_feed=VideoFeed(video_feed['feed_url']),
                dnn=self._generate_deep_neural_network(),
                websocket=self._websocket
            )
            self._video_feeds.append(processor)
        self._start_video_processors()


    def _add_video_feed(self, video_feed):
        """ Adds a video feed to the list of video feeds to be processed """
        video_processor = VideoProcessor(
            id=video_feed['id'],
            video_feed=VideoFeed(video_feed['feed_url']),
            dnn=self._generate_deep_neural_network(),
            websocket=self._websocket
        )
        video_processor.start()
        self._video_feeds.append(video_processor)
        
        
    def _remove_vide_feed(self, video_feed_id): # TODO: Delete video feed thread
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