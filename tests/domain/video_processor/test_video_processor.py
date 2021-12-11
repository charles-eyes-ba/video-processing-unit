from unittest import TestCase

from tests.mocks.mock_frame_collector import MockFrameCollector

class VideoProcessorTests(TestCase):
    
    def test_setup_callbacks(self):
        # Given
        video_capture = MockFrameCollector(None)
        video_feed = FrameCollectorImpl(video_capture)
        
        # When
        video_feed.setup_callbacks(on_error=lambda: None)
        
        # Then
        self.assertIsNotNone(video_feed._on_error)