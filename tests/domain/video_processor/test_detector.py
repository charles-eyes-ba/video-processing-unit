from unittest import TestCase
from unittest.mock import Mock
from time import sleep

from tests.mocks.mock_frame_collector import MockFrameCollector
from tests.mocks.mock_dnn import MockDeepNeuralNetwork
from src.domain.detector.detector_impl import DetectorImpl
from src.external.video_capture.exceptions import VideoCaptureConnectionLost

class DeteectorTests(TestCase):
    
    def test_setup_callbacks(self):
        # Given
        dnn = MockDeepNeuralNetwork('', '', '')
        frame_collector = MockFrameCollector(None)
        detector = DetectorImpl('id', frame_collector, dnn, delay=1)
        
        # When
        detector.setup_callbacks(on_object_detection=lambda x, y: None, on_error=lambda x, y: None)
        
        # Then
        self.assertIsNotNone(detector._on_object_detection)
        self.assertIsNotNone(detector._on_error)
        
        
    def test_start(self):
        # Given
        dnn = MockDeepNeuralNetwork('', '', '')
        frame_collector = MockFrameCollector(None)
        detector = DetectorImpl('id', frame_collector, dnn, delay=1)
        
        # When
        detector.start()
        
        # Then
        sleep(1)
        self.assertTrue(frame_collector.started)
        self.assertTrue(detector._is_running)
        self.assertTrue(detector._thread.is_alive())
        self.assertTrue(detector._thread.daemon)
        
    
    def test_stop(self):
        # Given
        dnn = MockDeepNeuralNetwork('', '', '')
        frame_collector = MockFrameCollector(None)
        detector = DetectorImpl('id', frame_collector, dnn, delay=1)
        
        # When
        detector.stop()
        
        # Then
        sleep(1)
        self.assertTrue(frame_collector.stopped)
        self.assertFalse(detector._is_running)
        self.assertFalse(detector._thread.is_alive())
        
        
    def test_dectection_object(self):
        # Given
        mock_object_detection = Mock()
        mock_error = Mock()
        dnn = MockDeepNeuralNetwork('', '', '')
        frame_collector = MockFrameCollector(None)
        detector = DetectorImpl('id', frame_collector, dnn, delay=1.1)
        detector.setup_callbacks(on_object_detection=mock_object_detection, on_error=mock_error)
        delay = 3
        
        # When
        detector.start()
        sleep(delay)
        detector.stop()
        
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
        detector = DetectorImpl('id', frame_collector, dnn, delay=0.2)
        detector.setup_callbacks(on_object_detection=mock_object_detection, on_error=mock_error)
        
        # When
        detector.start()
        sleep(1)
        detector.stop()
        
        # Then
        mock_object_detection.assert_not_called()
        mock_error.assert_not_called()
    
    
    def test_frame_none(self):
        # Given
        mock_object_detection = Mock()
        mock_error = Mock()
        dnn = MockDeepNeuralNetwork('', '', '')
        frame_collector = MockFrameCollector(None, pop_lastest_frame=lambda: None)
        detector = DetectorImpl('id', frame_collector, dnn, delay=0.1)
        detector.setup_callbacks(on_object_detection=mock_object_detection, on_error=mock_error)
        
        # When
        detector.start()
        sleep(1)
        detector.stop()
        
        # Then
        mock_object_detection.assert_not_called()
        mock_error.assert_not_called()    
    
    
    def test_exception_frame_collector(self):
        # Given
        mock_object_detection = Mock()
        mock_error = Mock()
        dnn = MockDeepNeuralNetwork('', '', '')
        frame_collector = MockFrameCollector(None)
        detector = DetectorImpl('id', frame_collector, dnn, delay=0.5)
        detector.setup_callbacks(on_object_detection=mock_object_detection, on_error=mock_error)
        
        # When
        detector.start()
        sleep(2)
        detector._on_frame_collector_error(VideoCaptureConnectionLost('Test Exception'))
        sleep(1)
        
        # Then
        mock_object_detection.assert_called()
        mock_error.assert_called()
        self.assertEqual(mock_error.call_args.args[0], 'id')
        self.assertIsInstance(mock_error.call_args.args[1], VideoCaptureConnectionLost)
        self.assertEqual(mock_error.call_args.args[1].message, 'Test Exception')
        self.assertTrue(frame_collector.stopped)
        self.assertFalse(detector._is_running)
        self.assertFalse(detector._thread.is_alive())