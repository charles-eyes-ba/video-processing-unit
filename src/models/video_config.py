class VideoConfig:
    """ Configuration to define which component should run """

    @staticmethod
    def all_disabled() -> 'VideoConfig':
        return VideoConfig(False, False)
        
    
    def __init__(self, run_frame_collector: bool, run_object_detector: bool):
        self.run_frame_collector = run_frame_collector
        self.run_object_detector = run_object_detector