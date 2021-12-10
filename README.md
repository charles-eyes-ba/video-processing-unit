# Video Processing Unit - VPU

The Video Processing Unit (A.k.a VPU) is the module that run the classification algorithms on the video feeds.

## Application Architecture 
<br/>
<p align="center">
  <img src="imgs/vpu.arch.png">
</p>

## Main Dependencies

| Module | Version |
| --- | --- |
| [OpenCV](https://github.com/opencv/opencv-python) | 4.5.4.60 |
| [Socket.IO](https://github.com/miguelgrinberg/python-socketio) | 5.5.0 |


## Setup
Create a `.env` file following the `.env.example` file.

## Start
To start the VPU you must install dependencies and run. You can do this with following command

```shell
$ pip install -r requirements.txt
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
