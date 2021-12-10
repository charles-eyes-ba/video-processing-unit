from src.configs.dnn_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.video_processor import VideoProcessor
from src.video_feed.video_feed import VideoFeed
from src.deep_neural_network.deep_neural_network import DeepNeuralNetwork
from src.websocket import WebSocketClient

from time import sleep

import logging
import asyncio

logging.basicConfig(level=logging.INFO)

class VideoProcessingUnit:
    """ 
    Class that handles the video processing unit 
    
    Methods
    -------
    start()
        Starts the video processing unit
    """
    
    DELAY_TO_RETRY_WEBSCOKET_CONNECTION = 30
    
    def __init__(self):
        self._websocket = None
        while self._websocket == None:
            try:
                self._websocket = WebSocketClient('http://0.0.0.0:1544')
                logging.info('Connected to websocket')
            except:
                delay = VideoProcessingUnit.DELAY_TO_RETRY_WEBSCOKET_CONNECTION
                logging.info(f'Trying to connect to websocket again in {delay} seconds...')
                sleep(delay)
                
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


    # * Websocekt Callbacks
    def _update_video_feed_list(self, video_feed_list):
        """ 
        Updates the list of video feeds to be processed 
        
        Parameters
        ----------
        video_feed_list : list
            The list of video feeds to be processed (replace all current video feeds)
        """
        self._video_feeds = []
        for video_feed in video_feed_list:
            self._add_video_feed(video_feed)


    def _add_video_feed(self, video_feed):
        """ 
        Adds a video feed to the list of video feeds to be processed 
        
        Parameters
        ----------
        video_feed : VideoFeed
            The video feed to be added
        """
        id = video_feed['id']
        url = video_feed['feed_url']
        video_processor = VideoProcessor(
            id=id,
            video_feed=VideoFeed(url),
            dnn=self._generate_deep_neural_network(),

            on_object_detection=self._on_detection_callback
        )
        logging.info(f'Adding video feed {id} with url {url}')
        video_processor.start()
        logging.info(f'Started video feed {id} with url {url}')
        self._video_feeds.append(video_processor)
        
        
    def _remove_vide_feed(self, video_feed_id): # TODO: Delete video feed thread
        """ 
        Removes a video feed from the list of video feeds to be processed 
        
        Parameters
        ----------
        video_feed_id : int
            The id of the video feed to be removed
        """
        for video in self._video_feeds:
            if video.id == video_feed_id:
                self._video_feeds.remove(video)
                break
    
    
    # * Video Processor Callbacks
    def _on_detection_callback(self, id, classes):
        """ 
        Callback for when a detection is made for a video feed
        
        Parameters
        ----------
        id : str
            The id of the video feed
        classes : list
            The list of classes detected
        """
        self._websocket.send_detections(id, classes)
    
    
    # * Starts
    def _start_video_processors(self):
        """ Starts all video feeds processing """
        for video_feed in self._video_feeds:
            video_feed.start()
    
    
    def start(self):
        """ Starts video processing unit aplication """
        self._start_video_processors()
        asyncio.get_event_loop().run_forever()