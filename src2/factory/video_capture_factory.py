from src2.external.video_capture.video_capture_opencv import VideoCaptureOpenCV

def create_video_capture(url):
    return VideoCaptureOpenCV(url)