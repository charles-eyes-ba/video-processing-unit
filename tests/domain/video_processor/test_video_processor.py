from unittest import TestCase
from unittest.mock import Mock
from time import sleep
from datetime import datetime

from tests.mocks.mock_frame_collector import MockFrameCollector
from tests.mocks.mock_dnn import MockDeepNeuralNetwork
from src.domain.video_processor.video_processor_impl import VideoProcessorImpl
from src.external.video_capture.exceptions import VideoCaptureConnectionLost

import numpy

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
        # Given
        mock_object_detection = Mock()
        mock_error = Mock()
        dnn = MockDeepNeuralNetwork('', '', '')
        frame_collector = MockFrameCollector(None)
        video_processor = VideoProcessorImpl('id', frame_collector, dnn, delay=1.1)
        video_processor.setup_callbacks(on_object_detection=mock_object_detection, on_error=mock_error)
        delay = 3
        
        # When
        video_processor.start()
        sleep(delay)
        video_processor.stop()
        
        # Then
        mock_object_detection.assert_called()
        mock_error.assert_not_called()
        self.assertEqual(mock_object_detection.call_count, 3)
        self.assertEqual(mock_object_detection.call_args.args, ('id', [2]))
    
    
    def test_empty_detection(self):
        # Given
        mock_object_detection = Mock()
        mock_error = Mock()
        dnn = MockDeepNeuralNetwork('', '', '', predict=lambda x: ([], [], []))
        frame_collector = MockFrameCollector(None)
        video_processor = VideoProcessorImpl('id', frame_collector, dnn, delay=0.2)
        video_processor.setup_callbacks(on_object_detection=mock_object_detection, on_error=mock_error)
        
        # When
        video_processor.start()
        sleep(1)
        video_processor.stop()
        
        # Then
        mock_object_detection.assert_not_called()
        mock_error.assert_not_called()
    
    
    def test_frame_none(self):
        # Given
        mock_object_detection = Mock()
        mock_error = Mock()
        dnn = MockDeepNeuralNetwork('', '', '')
        frame_collector = MockFrameCollector(None, pop_lastest_frame=lambda: None)
        video_processor = VideoProcessorImpl('id', frame_collector, dnn, delay=0.1)
        video_processor.setup_callbacks(on_object_detection=mock_object_detection, on_error=mock_error)
        
        # When
        video_processor.start()
        sleep(1)
        video_processor.stop()
        
        # Then
        mock_object_detection.assert_not_called()
        mock_error.assert_not_called()    
    
    
    def test_exception_frame_collector(self):
        # Given
        mock_object_detection = Mock()
        mock_error = Mock()
        dnn = MockDeepNeuralNetwork('', '', '')
        frame_collector = MockFrameCollector(None)
        video_processor = VideoProcessorImpl('id', frame_collector, dnn, delay=0.5)
        video_processor.setup_callbacks(on_object_detection=mock_object_detection, on_error=mock_error)
        
        # When
        video_processor.start()
        sleep(2)
        video_processor._on_frame_collector_error(VideoCaptureConnectionLost('Test Exception'))
        sleep(1)
        
        # Then
        mock_object_detection.assert_called()
        mock_error.assert_called()
        self.assertEqual(mock_error.call_args.args[0], 'id')
        self.assertIsInstance(mock_error.call_args.args[1], VideoCaptureConnectionLost)
        self.assertEqual(mock_error.call_args.args[1].message, 'Test Exception')
        self.assertTrue(frame_collector.stopped)
        self.assertFalse(video_processor._is_running)
        self.assertFalse(video_processor._thread.is_alive())