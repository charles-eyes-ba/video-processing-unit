from unittest import TestCase
from time import sleep

from tests.mocks.mock_frame_collector import MockFrameCollector
from tests.mocks.mock_dnn import MockDeepNeuralNetwork
from src.domain.video_processor.video_processor_impl import VideoProcessorImpl

class VideoProcessorTests(TestCase):
    
    def test_setup_callbacks(self):
        # Given
        dnn = MockDeepNeuralNetwork('', '', '')
        frame_collector = MockFrameCollector(None)
        video_processor = VideoProcessorImpl('id', frame_collector, dnn, delay=1)
        
        # When
        video_processor.setup_callbacks(on_object_detection=lambda x, y: None, on_error=lambda x, y: None)
        
        # Then
        self.assertIsNotNone(video_processor._on_object_detection)
        self.assertIsNotNone(video_processor._on_error)
        
        
    def test_start(self):
        # Given
        dnn = MockDeepNeuralNetwork('', '', '')
        frame_collector = MockFrameCollector(None)
        video_processor = VideoProcessorImpl('id', frame_collector, dnn, delay=1)
        
        # When
        video_processor.start()
        
        # Then
        sleep(1)
        self.assertTrue(frame_collector.started)
        self.assertTrue(video_processor._is_running)
        self.assertTrue(video_processor._thread.is_alive())
        self.assertTrue(video_processor._thread.daemon)
        
    
    def test_stop(self):
        # Given
        dnn = MockDeepNeuralNetwork('', '', '')
        frame_collector = MockFrameCollector(None)
        video_processor = VideoProcessorImpl('id', frame_collector, dnn, delay=1)
        
        # When
        video_processor.stop()
        
        # Then
        sleep(1)
        self.assertTrue(frame_collector.stopped)
        self.assertFalse(video_processor._is_running)
        self.assertFalse(video_processor._thread.is_alive())
        
        
    def test_dectection_object(self):
        pass
    
    
    def test_empty_detection(self):
        pass
    
    
    def test_frame_none(self):
        pass
    
    
    def test_exception_frame_collector(self):
        pass