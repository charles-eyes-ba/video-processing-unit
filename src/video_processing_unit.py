from src.configs.dnn_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.video_processor import VideoProcessor
from src.video_feed.video_feed import VideoFeed
from src.deep_neural_network.deep_neural_network import DeepNeuralNetwork
from src.websocket import WebSocketClient
from src.configs.environment import HSU_WEBSOCKET_URL

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
        self._websocket = WebSocketClient()
        while True:
            try:
                self._websocket.connect(HSU_WEBSOCKET_URL)
                logging.info('Connected to websocket')
                break
            except:
                delay = VideoProcessingUnit.DELAY_TO_RETRY_WEBSCOKET_CONNECTION
                logging.info(f'Trying to connect to websocket again in {delay} seconds...')
                sleep(delay)
        
        self._video_feeds = []        
        self._setup_websocket_callbacks()
        self._websocket.request_configs()


    # * Setups
    def _setup_websocket_callbacks(self):
        """ Sets up the websocket client """
        self._websocket.on_video_feeds_update = self._update_video_feed_list
        self._websocket.on_add_video_feed = self._add_video_feed
        self._websocket.on_remove_video_feed = self._remove_video_feed
        # TODO: Handle disconect event
        
    
    # * Generators
    def _generate_deep_neural_network(self):
        """ Generates a deep neural network """
        return DeepNeuralNetwork(
            config_path=YOLO_CONFIG_PATH, 
            weights_path=YOLO_WEIGHTS_PATH, 
            classes_path=YOLO_CLASSES_PATH
        )
        
        
    def _generate_video_feed(self, id, url):
        """ 
        Generates a video feed 
        
        Parameters
        ----------
        id : str
            The id of the camera
        url : str
            The url of the video feed
        """
        return VideoFeed(
            id=id,
            feed_url=url,
            on_connection_error=self._on_video_feed_connection_error,
        )


    def _generate_video_processor(self, id, url):
        """ 
        Generates a video processor
        
        Parameters
        ----------
        id : str
            The id of the camera
        url : str
            The url of the video feed
        """
        return VideoProcessor(
            id=id,
            video_feed=self._generate_video_feed(id, url),
            dnn=self._generate_deep_neural_network(),
            on_object_detection=self._on_detection_callback,
        )


    # * Websocket Callbacks
    def _update_video_feed_list(self, video_feed_list):
        """ 
        Updates the list of video feeds to be processed 
        
        Parameters
        ----------
        video_feed_list : list
            The list of video feeds to be processed (replace all current video feeds)
        """
        logging.info('Updating all video feed list')
        self._video_feeds = [] # TODO: Remove all video feeds and kill all threads
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
        id = video_feed['id'] # TODO: Handler nullable id
        url = video_feed['feed_url'] # TODO: Handler nullable feed_url
        
        logging.info(f'Adding video feed {id} with url {url}')
        video_processor = self._generate_video_processor(id, url)
        logging.info(f'Starting video feed {id} with url {url}')
        video_processor.start()
        self._video_feeds.append(video_processor)
        
        
    def _remove_video_feed(self, video_feed_id):
        """ 
        Removes a video feed from the list of video feeds to be processed 
        
        Parameters
        ----------
        video_feed_id : int
            The id of the video feed to be removed
        """
        for video in self._video_feeds:
            if video.id == video_feed_id:
                logging.info(f'Removing {video_feed_id} video feed')
                self._video_feeds.remove(video) # TODO: Kill video feed thread and video processor thread
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
    
    
    # * Video Feeds Callbacks
    def _on_video_feed_connection_error(self, id, exception):
        """
        Callback for when a video feed connection error occurs
        
        Parameters
        ----------
        id : str
            The id of the video feed
        exception : Exception
            The exception that occurred
        """
        logging.error(f'Video feed {id} connection error: {exception}')
        self._remove_video_feed(id)
    
    
    # * Starts
    def start(self):
        """ Starts video processing unit aplication """
        logging.info('Starting video processing unit')
        asyncio.get_event_loop().run_forever()