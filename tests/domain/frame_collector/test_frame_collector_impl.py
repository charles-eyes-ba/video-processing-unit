from unittest import TestCase
from unittest.mock import Mock
from time import sleep
from datetime import datetime

from tests.mocks.mock_video_capture import MockVideoCapture
from src.domain.frame_collector.frame_collector_impl import FrameCollectorImpl
from src.external.video_capture.exceptions import VideoCaptureConnectionLost

import numpy
import logging

logging.disable()

class FrameCollectorImplTests(TestCase):
    
    # * Useful Functions to Mock
    def generate_frame(class_instance):
        second = datetime.now().second
        fake_image = numpy.ndarray([3, 3, 3])
        value_to_fill = second if second % 2 == 0 else int(second / 2)
        fake_image.fill(value_to_fill)
        return fake_image
    
    
    def throw_exception(self):
        raise VideoCaptureConnectionLost('Test Exception')
    
    
    # * Tests
    def test_frame_collector_setup_callbacks(self):
        # Given
        video_capture = MockVideoCapture('')
        frame_collector = FrameCollectorImpl(video_capture)
        
        # When
        frame_collector.setup_callbacks(on_error=lambda: None)
        
        # Then
        self.assertIsNotNone(frame_collector._on_error)
        
    
    def test_frame_collector_start(self):
        # Given
        video_capture = MockVideoCapture('')
        frame_collector = FrameCollectorImpl(video_capture)
        
        # When
        frame_collector.start()
        
        # Then
        sleep(1)
        self.assertTrue(frame_collector._is_running)
        self.assertTrue(frame_collector._thread.is_alive())
        self.assertTrue(frame_collector._thread.daemon)
        
    
    def test_frame_collector_stop(self):
        # Given
        video_capture = MockVideoCapture('')
        frame_collector = FrameCollectorImpl(video_capture)
        frame_collector.start()
        
        # When
        frame_collector.stop()
        
        # Then
        sleep(1)
        self.assertFalse(frame_collector._is_running)
        self.assertFalse(frame_collector._thread.is_alive())
        
        
    def test_frame_collector_pop_lastest_frame(self):
        # Given
        video_capture = MockVideoCapture('', read=self.generate_frame)
        frame_collector = FrameCollectorImpl(video_capture)
        second = datetime.now().second
        frame_collector.start()
        delay = 5
        
        # When
        sleep(delay)
        frame = frame_collector.pop_lastest_frame()
        
        # Then
        second_reference = (second + delay) % 60
        frame_value = second_reference if second_reference % 2 == 0 else int(second_reference / 2)
        
        self.assertEqual(frame.max(), frame_value)
        
        
    def test_frame_collector_release(self):
        # Given
        video_capture = MockVideoCapture('')
        frame_collector = FrameCollectorImpl(video_capture)
        
        # When
        frame_collector.release()
        
        # Then
        self.assertFalse(frame_collector._is_running)
        self.assertTrue(video_capture.released)
        
        
    def test_frame_collector_exception_conection_lost(self):
        # Given
        mock = Mock()
        video_capture = MockVideoCapture('', read=self.throw_exception)
        frame_collector = FrameCollectorImpl(video_capture)
        frame_collector.setup_callbacks(on_error=mock)
        
        # When
        frame_collector.start()
        sleep(1)
        
        # Then
        self.assertFalse(frame_collector._is_running)
        self.assertTrue(video_capture.released)
        self.assertIsInstance(mock.call_args.args[0], VideoCaptureConnectionLost)
        self.assertEqual(mock.call_args.args[0].message, 'Test Exception')
        mock.assert_called_once()