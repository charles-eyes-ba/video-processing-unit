from src.domain.configs.cams import CAM_HOUSE_EXTERNAL_RIGHT, CAM_HOUSE_EXTERNAL_LEFT, CAM_HOUSE_GARAGE, CAM_HOUSE_BACKYARD
from src.domain.configs.dnn_paths import YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH

from src.external.opencv.video_feed import VideoFeed
from src.external.opencv.deep_neural_network import DeepNeuralNetwork

from src.domain.video_processor import VideoProcessor

# Setup Video Processors
camera_1 = VideoProcessor(
    id="CAM_HOUSE_EXTERNAL_RIGHT",
    cam=VideoFeed(CAM_HOUSE_EXTERNAL_RIGHT),
    yolo=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)
)

camera_2 = VideoProcessor(
    id="CAM_HOUSE_EXTERNAL_LEFT",
    cam=VideoFeed(CAM_HOUSE_EXTERNAL_LEFT),
    yolo=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)
)

camera_3 = VideoProcessor(
    id="CAM_HOUSE_GARAGE",
    cam=VideoFeed(CAM_HOUSE_GARAGE),
    yolo=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)
)

camera_4 = VideoProcessor(
    id="CAM_HOUSE_BACKYARD",
    cam=VideoFeed(CAM_HOUSE_BACKYARD),
    yolo=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)
)

camera_5 = VideoProcessor(
    id="CAM_HOUSE_BACKYARD_5",
    cam=VideoFeed(CAM_HOUSE_BACKYARD),
    yolo=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)
)

camera_6 = VideoProcessor(
    id="CAM_HOUSE_BACKYARD_6",
    cam=VideoFeed(CAM_HOUSE_BACKYARD),
    yolo=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)
)

camera_7 = VideoProcessor(
    id="CAM_HOUSE_BACKYARD_7",
    cam=VideoFeed(CAM_HOUSE_BACKYARD),
    yolo=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)
)

camera_8 = VideoProcessor(
    id="CAM_HOUSE_BACKYARD_8",
    cam=VideoFeed(CAM_HOUSE_BACKYARD),
    yolo=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)
)


from time import sleep
while True:
    sleep(100)