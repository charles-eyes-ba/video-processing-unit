from unittest import TestCase
from unittest.mock import Mock
from time import sleep
from datetime import datetime

from tests.mocks.mock_video_capture import MockVideoCapture
from src.domain.frame_collector.frame_collector_impl import FrameCollectorImpl
from src.external.video_capture.exceptions import VideoCaptureConnectionLost

import numpy

class FrameCollectorImplTests(TestCase):
    
    # * Useful Functions to Mock
    def generate_frame(class_instance):
        second = datetime.now().second
        fake_image = numpy.ndarray([3, 3, 3])
        value_to_fill = second if second % 2 == 0 else second + 1
        fake_image.fill(value_to_fill)
        return fake_image
    
    
    def throw_exception(self):
        raise VideoCaptureConnectionLost('Test Exception')
    
    
    # * Tests
    def test_setup_callbacks(self):
        # Given
        video_capture = MockVideoCapture('')
        video_feed = FrameCollectorImpl(video_capture)
        
        # When
        video_feed.setup_callbacks(on_error=lambda: None)
        
        # Then
        self.assertIsNotNone(video_feed._on_error)
        
    
    def test_start(self):
        # Given
        video_capture = MockVideoCapture('')
        video_feed = FrameCollectorImpl(video_capture)
        
        # When
        video_feed.start()
        
        # Then
        sleep(1)
        self.assertTrue(video_feed._is_running)
        self.assertTrue(video_feed._thread.is_alive())
        self.assertTrue(video_feed._thread.daemon)
        
    
    def test_stop(self):
        # Given
        video_capture = MockVideoCapture('')
        video_feed = FrameCollectorImpl(video_capture)
        video_feed.start()
        
        # When
        video_feed.stop()
        
        # Then
        sleep(1)
        self.assertFalse(video_feed._is_running)
        self.assertFalse(video_feed._thread.is_alive())
        
        
    def test_pop_lastest_frame(self):
        # Given
        video_capture = MockVideoCapture('', read=self.generate_frame)
        video_feed = FrameCollectorImpl(video_capture)
        second = datetime.now().second
        video_feed.start()
        delay = 5
        
        # When
        sleep(delay)
        frame = video_feed.pop_lastest_frame()
        
        # Then
        second_reference = (second + delay) % 60
        frame_value = second_reference if second_reference % 2 == 0 else second_reference + 1
        
        self.assertEqual(frame.max(), frame_value)
        
        
    def test_release(self):
        # Given
        video_capture = MockVideoCapture('')
        video_feed = FrameCollectorImpl(video_capture)
        
        # When
        video_feed.release()
        
        # Then
        self.assertFalse(video_feed._is_running)
        self.assertTrue(video_capture.released)
        
        
    def test_exception_conection_lost(self):
        # Given
        mock = Mock()
        video_capture = MockVideoCapture('', read=self.throw_exception)
        video_feed = FrameCollectorImpl(video_capture)
        video_feed.setup_callbacks(on_error=mock)
        
        # When
        video_feed.start()
        sleep(1)
        
        # Then
        self.assertFalse(video_feed._is_running)
        self.assertTrue(video_capture.released)
        self.assertIsInstance(mock.call_args.args[0], VideoCaptureConnectionLost)
        self.assertEqual(mock.call_args.args[0].message, 'Test Exception')
        mock.assert_called_once()