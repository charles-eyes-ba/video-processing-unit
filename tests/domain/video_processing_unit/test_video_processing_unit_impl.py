from unittest import TestCase

from src.external.deep_neural_network.exceptions import InvalidDeepNeuralNetworkFilesException
from src.domain.video_processing_unit.exceptions import CameraParamsNotFoundException

from src.domain.video_processing_unit.video_processing_unit_impl import VideoProcessingUnitImpl
from tests.mocks.mock_video_capture import MockVideoCapture
from tests.mocks.mock_frame_collector import MockFrameCollector
from tests.mocks.mock_detector import MockDetector
from tests.mocks.mock_websocket import MockWebSocket

import logging

logging.disable()

class VideoProcessingUnitTests(TestCase):
    
    # * Useful Functions to Mock
    def generate_mock_detector(self, id, url, config_path,  weights_path,  classes_path):
        video_capture = MockVideoCapture(url)
        frame_collector = MockFrameCollector(video_capture)
        detector = MockDetector(id, frame_collector, None, url)
        return detector
    
    
    # * Tests
    def test_vpu_connect(self):
        # Given
        websocket = MockWebSocket()
        vpu = VideoProcessingUnitImpl(websocket, self.generate_mock_detector)
        vpu._detectors = [
            self.generate_mock_detector('1', 'https://google.com', '', '', ''),
            self.generate_mock_detector('2', 'https://charles.com', '', '', ''),
        ]
        
        # When
        vpu._on_connect()
        
        # Then
        self.assertTrue(websocket.requested_config)
        
        
    def test_vpu_disconnect(self):
        # Given
        websocket = MockWebSocket()
        vpu = VideoProcessingUnitImpl(websocket, self.generate_mock_detector)
        video_feeds = [
            { 'id': '1', 'feed_url': 'https://google.com' },
            { 'id': '2', 'feed_url': 'https://charles.com' },
        ]
        vpu._update_video_feed_list(video_feeds)
        
        # When
        vpu._on_disconnect()
        
        # Then
        self.assertEqual(len(vpu._detectors), 2)
        self.assertTrue(vpu._detectors[0].stopped)
        self.assertTrue(vpu._detectors[1].stopped)
        
    
    def test_vpu_add_video_feed(self):
        # Given
        websocket = MockWebSocket()
        vpu = VideoProcessingUnitImpl(websocket, self.generate_mock_detector)
        video_feed_to_add = { 'id': '1', 'feed_url': 'https://google.com' }
        
        # When
        vpu._add_video_feed(video_feed_to_add)
        
        # Then
        self.assertEqual(len(vpu._detectors), 1)
        self.assertEqual(vpu._detectors[0].id, '1')
        self.assertEqual(vpu._detectors[0]._frame_collector._video_capture.url, 'https://google.com')
        self.assertIsNotNone(vpu._detectors[0]._on_object_detection)
        self.assertIsNotNone(vpu._detectors[0]._on_error)
    
    
    def test_vpu_add_video_same_id_in_list(self):
        # Given
        websocket = MockWebSocket()
        vpu = VideoProcessingUnitImpl(websocket, self.generate_mock_detector)
        video_feed_to_start = { 'id': '1', 'feed_url': 'https://google.com' }
        vpu._add_video_feed(video_feed_to_start)
        video_feed_to_add = { 'id': '1', 'feed_url': 'https://charles.com' }
        
        # When
        vpu._add_video_feed(video_feed_to_add)
        
        # Then
        self.assertEqual(len(vpu._detectors), 1)
        self.assertEqual(vpu._detectors[0].id, '1')
        self.assertEqual(vpu._detectors[0]._frame_collector._video_capture.url, 'https://google.com')
    
    
    def test_vpu_add_video_feed_without_id(self):
        # Given
        websocket = MockWebSocket()
        vpu = VideoProcessingUnitImpl(websocket, self.generate_mock_detector)
        video_feed_to_add = { 'feed_url': 'https://google.com' }
        
        # When
        vpu._add_video_feed(video_feed_to_add)
        
        # Then
        self.assertEqual(len(vpu._detectors), 0)
        self.assertTrue(websocket.sent_error)
        self.assertEqual(websocket.sent_error_params[0], 'None')
        self.assertIsInstance(websocket.sent_error_params[1], CameraParamsNotFoundException)
        self.assertEqual(websocket.sent_error_params[1].message, 'Not found id')
        
        
    def test_vpu_add_video_feed_without_url(self):
        # Given
        websocket = MockWebSocket()
        vpu = VideoProcessingUnitImpl(websocket, self.generate_mock_detector)
        video_feed_to_add = { 'id': '1' }
        
        # When
        vpu._add_video_feed(video_feed_to_add)
        
        # Then
        self.assertEqual(len(vpu._detectors), 0)
        self.assertTrue(websocket.sent_error)
        self.assertEqual(websocket.sent_error_params[0], 'None')
        self.assertIsInstance(websocket.sent_error_params[1], CameraParamsNotFoundException)
        self.assertEqual(websocket.sent_error_params[1].message, 'Not found feed_url')
        
        
    def test_vpu_add_video_feed_with_error_in_create_detector(self):
        # Given
        def throw_exception_creation(id, url, config_path,  weights_path,  classes_path):
            raise InvalidDeepNeuralNetworkFilesException('Test Exception')
        websocket = MockWebSocket()
        vpu = VideoProcessingUnitImpl(websocket, throw_exception_creation)
        video_feed_to_add = { 'id': '1', 'feed_url': 'https://google.com' }
        
        # When
        vpu._add_video_feed(video_feed_to_add)
        
        # Then
        self.assertEqual(len(vpu._detectors), 0)
        self.assertTrue(websocket.sent_error)
        self.assertEqual(websocket.sent_error_params[0], '1')
        self.assertIsInstance(websocket.sent_error_params[1], InvalidDeepNeuralNetworkFilesException)
        self.assertEqual(websocket.sent_error_params[1].message, 'Test Exception')
        
    
    def test_vpu_remove_video_feed(self):
        # Given
        websocket = MockWebSocket()
        vpu = VideoProcessingUnitImpl(websocket, self.generate_mock_detector)
        video_feed = { 'id': '1', 'feed_url': 'https://google.com' }
        vpu._add_video_feed(video_feed)
        
        # When
        vpu._remove_video_feed('1')
        
        # Then
        self.assertEqual(len(vpu._detectors), 0)
    
    
    def test_vpu_remove_video_feed_without_id_in_list(self):
        # Given
        websocket = MockWebSocket()
        vpu = VideoProcessingUnitImpl(websocket, self.generate_mock_detector)
        video_feed = { 'id': '1', 'feed_url': 'https://google.com' }
        vpu._add_video_feed(video_feed)
        
        # When
        vpu._remove_video_feed('2')
        
        # Then
        self.assertEqual(len(vpu._detectors), 1)
    
    
    def test_vpu_update_video_feed_list_with_empty_list(self):
        # Given
        websocket = MockWebSocket()
        vpu = VideoProcessingUnitImpl(websocket, self.generate_mock_detector)
        video_feeds = [
            { 'id': '1', 'feed_url': 'https://google.com' },
            { 'id': '2', 'feed_url': 'https://charles.com' },
        ]
        
        # When
        vpu._update_video_feed_list(video_feeds)
        
        # Then
        self.assertEqual(len(vpu._detectors), 2)
        self.assertEqual(vpu._detectors[0].id, '1')
        self.assertEqual(vpu._detectors[0]._frame_collector._video_capture.url, 'https://google.com')
        self.assertIsNotNone(vpu._detectors[0]._on_object_detection)
        self.assertIsNotNone(vpu._detectors[0]._on_error)
        self.assertEqual(vpu._detectors[1].id, '2')
        self.assertEqual(vpu._detectors[1]._frame_collector._video_capture.url, 'https://charles.com')
        self.assertIsNotNone(vpu._detectors[1]._on_object_detection)
        self.assertIsNotNone(vpu._detectors[1]._on_error)
        
        
    def test_vpu_update_video_feed_list_with_non_empty_list(self):
        # Given
        websocket = MockWebSocket()
        vpu = VideoProcessingUnitImpl(websocket, self.generate_mock_detector)
        video_feed = { 'id': '1', 'feed_url': 'https://google.com' }
        vpu._add_video_feed(video_feed)
        video_feeds = [
            { 'id': '1', 'feed_url': 'https://google.com' },
            { 'id': '2', 'feed_url': 'https://charles.com' },
        ]
        
        # When
        vpu._update_video_feed_list(video_feeds)
        
        # Then
        self.assertEqual(len(vpu._detectors), 2)
        self.assertEqual(vpu._detectors[0].id, '1')
        self.assertEqual(vpu._detectors[0]._frame_collector._video_capture.url, 'https://google.com')
        self.assertIsNotNone(vpu._detectors[0]._on_object_detection)
        self.assertIsNotNone(vpu._detectors[0]._on_error)
        self.assertEqual(vpu._detectors[1].id, '2')
        self.assertEqual(vpu._detectors[1]._frame_collector._video_capture.url, 'https://charles.com')
        self.assertIsNotNone(vpu._detectors[1]._on_object_detection)
        self.assertIsNotNone(vpu._detectors[1]._on_error)
        
        
    def test_vpu_detection_callback(self):
        # Given
        websocket = MockWebSocket()
        vpu = VideoProcessingUnitImpl(websocket, self.generate_mock_detector)
        
        # When
        vpu._on_detection_callback('1', ['car'])
        
        # Then
        self.assertTrue(websocket.sent_detections, '1')
        self.assertEqual(websocket.sent_detections_params[0], '1')
        self.assertEqual(websocket.sent_detections_params[1], ['car'])
        
        
    def test_vpu_error_callback(self):
        # Given
        websocket = MockWebSocket()
        vpu = VideoProcessingUnitImpl(websocket, self.generate_mock_detector)
        
        # When
        vpu._on_error_callback('1', CameraParamsNotFoundException('Test Exception'))
        
        # Then
        self.assertTrue(websocket.sent_error)
        self.assertEqual(websocket.sent_error_params[0], '1')
        self.assertIsInstance(websocket.sent_error_params[1], CameraParamsNotFoundException)
        self.assertEqual(websocket.sent_error_params[1].message, 'Test Exception')