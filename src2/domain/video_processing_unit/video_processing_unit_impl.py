from src2.common.dnn_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH
from src2.common.environment import HSU_WEBSOCKET_URL
from .exceptions import CameraParamsNotFoundException
from .interface import VideoProcessingUnit

from time import sleep

import logging
import asyncio

class VideoProcessingUnitImpl(VideoProcessingUnit):
    def __init__(self, websocket, create_detector):
        self._detectors = []
        self._create_detector = create_detector
        self._websocket = websocket
        self.__setup_websocket_callbacks()
        
        delay_to_retry = 5
        while True:
            try:
                self._websocket.connect(HSU_WEBSOCKET_URL)
                logging.info('Connected to websocket')
                break
            except:
                logging.info(f'Trying to connect to websocket again in {delay_to_retry} seconds...')
                sleep(delay_to_retry)


    # * Setups
    def __setup_websocket_callbacks(self):
        self._websocket.setup_callbacks(
            on_connect=self._on_connect,
            on_disconnect=self._on_disconnect,
            on_video_feeds_update=self._update_video_feed_list, 
            on_add_video_feed=self._add_video_feed, 
            on_remove_video_feed=self._remove_video_feed
        )
            

    # * Websocket Callbacks
    def _on_connect(self):
        logging.info('Restarting VPU and getting updated video feed list')
        self._websocket.request_configs()
            
            
    def _on_disconnect(self):
        logging.info('Pausing all detectors')
        for detector in self._detectors:
            detector.stop()
    
    
    def _add_video_feed(self, video_feed):
        try:
            id = video_feed['id']
            url = video_feed['feed_url']
        except KeyError as e:
            key_empty = e.args[0]
            self._on_error_callback('None', CameraParamsNotFoundException(f'Not found {key_empty}'))
            return
        
        if any(detector.id == id for detector in self._detectors):
            logging.info(f'Video feed {id} already exists')
            return
        
        try:
            logging.info(f'Adding video feed {id} with url {url}')
            detector = self._create_detector(
                id=id,
                url=url,
                config_path=YOLO_CONFIG_PATH, 
                weights_path=YOLO_WEIGHTS_PATH, 
                classes_path=YOLO_CLASSES_PATH
            )    
        except Exception as e:
            self._on_error_callback(id, e)
            return
        
        detector.setup_callbacks(
            on_object_detection=self._on_detection_callback,
            on_error=self._on_error_callback
        )
        logging.info(f'Starting video feed {id} with url {url}')
        detector.start()
        self._detectors.append(detector)
        
        
    def _remove_video_feed(self, video_feed_id):
        for detector in self._detectors:
            if detector.id == video_feed_id:
                logging.info(f'Removing {video_feed_id} video feed')
                detector.stop()
                self._detectors.remove(detector)
                break
    
    
    def _update_video_feed_list(self, video_feed_list):
        logging.info('Cleaning all video feed list')
        for detector in self._detectors:
            detector.stop()
            
        logging.info('Updating all video feed list')
        self._detectors = []
        for video_feed in video_feed_list:
            self._add_video_feed(video_feed)
    
    
    # * Video Processor Callbacks
    def _on_detection_callback(self, id, classes):
        logging.debug(f'Detection in {id} | Classes: {classes}')
        self._websocket.send_detections(id, classes)
    
    
    def _on_error_callback(self, id, exception):
        logging.error(f'Error in video feed {id}')
        self._websocket.send_error(id, exception)
    
    
    # * Starts
    def start(self):
        logging.info('Starting video processing unit')
        asyncio.get_event_loop().run_forever()