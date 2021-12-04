from src.app import VideoProcessingUnit

vpu = VideoProcessingUnit()
vpu.start()

# camera_1 = VideoProcessor(
#     id="CAM_HOUSE_EXTERNAL_RIGHT",
#     video_feed=VideoFeed(CAM_HOUSE_EXTERNAL_RIGHT),
#     dnn=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH),
#     websocket=websocket
# )

# camera_2 = VideoProcessor(
#     id="CAM_HOUSE_EXTERNAL_LEFT",
#     video_feed=VideoFeed(CAM_HOUSE_EXTERNAL_LEFT),
#     dnn=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH),
#     websocket=websocket
# )

# camera_3 = VideoProcessor(
#     id="CAM_HOUSE_GARAGE",
#     video_feed=VideoFeed(CAM_HOUSE_GARAGE),
#     dnn=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH),
#     websocket=websocket
# )

# camera_4 = VideoProcessor(
#     id="CAM_HOUSE_BACKYARD",
#     video_feed=VideoFeed(CAM_HOUSE_BACKYARD),
#     dnn=DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH),
#     websocket=websocket
# )