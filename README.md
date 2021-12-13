# Video Processing Unit - VPU

The Video Processing Unit (A.k.a VPU) is the module that run the classification algorithms on the video feeds.

## Architecture 

### Application

The VPU is a module that among several that represent the Home Security application. The diagram below represents the components that directly interact with the VPU in the application's macro architecture.

<br/>
<p align="center">
  <img src="imgs/HS.png">
</p>


### Project

This diagram represents a bit of the architecture of how the VPU was built. It has 3 main components, these being: Video Capture, Detector and the Video Processing Unit (VPU).

<br/>
<p align="center">
  <img src="imgs/VPU.png">
</p>

- __Video Capture__: This component ensures that the most recent frame of a video feed is always available. For each video feed it is created.
- __Detector__: This component obtains the most recent frame made available by video capture and detects the objects present in the frame. This process keeps repeating itself with a delay. For each prediction it informs the VPU that there have been new detections.
- __Video Processing Unit__: This component manages several detectors, one for each video feed provided. The detections or errors will be transferred to the Home Security Unit (HSU). This is where detectors are created or removed. All this communication with the HSU is done via Websocket.

## Main Dependencies

| Module | Version |
| --- | --- |
| [OpenCV](https://github.com/opencv/opencv-python) | 4.5.4.60 |
| [Socket.IO](https://github.com/miguelgrinberg/python-socketio) | 5.5.0 |


## Setup

Create a `.env` file following the `.env.example` file.

### Install Dependencies

It is recommended that a virtual environment be used for the project. If you want to use venv, just type:

```shell
$ python -m venv .venv
```

And to start virtual environment:

```shell
$ source .venv/bin/activate
```

To install dependencies:

```shell
$ pip install -r requirements.txt
```

### Start 
To start the VPU, you can do this with following command (run `main.py`):

```shell
$ python main.py
```

## Debugging
- Show the video feed with boxes

```python
from src.deep_neural_network import DeepNeuralNetwork
from src.configs.dnn_paths import YOLO_CLASSES_PATH, YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH
import cv2

cams = [cv2.VideoCapture(<URL>)]
dnn = DeepNeuralNetwork(YOLO_CONFIG_PATH, YOLO_WEIGHTS_PATH, YOLO_CLASSES_PATH)

while True:
    for index, camera in enumerate(cams):
        ret, frame = camera.read()

        if not ret:
            continue
        
        boxes, scores, classes = dnn.predict(frame)
        dnn.show_img_with_boxes(str(index), frame, boxes, scores, classes, scale=2)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```
