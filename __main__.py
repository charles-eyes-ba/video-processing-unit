from src.factory import vpu_factory, websocket_factory, video_capture_factory, frame_collector_factory, detector_factory, dnn_factory
import logging

logging.basicConfig(level=logging.DEBUG)

# Main
def create_detector(id, url, config_path,  weights_path,  classes_path):
    video_capture = video_capture_factory.create_video_capture(url)
    frame_collector = frame_collector_factory.create_frame_collector(video_capture)
    dnn = dnn_factory.create_dnn(config_path, weights_path, classes_path)
    return detector_factory.create_detector(id, frame_collector, dnn)

if __name__ == '__main__':
    websocket = websocket_factory.create_websocket()
    vpu = vpu_factory.create_vpu(websocket, create_detector)
    vpu.start()