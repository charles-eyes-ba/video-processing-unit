# Video Processing Unit - VPU
[![Unit Tests](https://github.com/charles-eyes-ba/video-processing-unit/actions/workflows/python-test.yml/badge.svg)](https://github.com/charles-eyes-ba/video-processing-unit/actions/workflows/python-test.yml)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-360)
![Coverage](imgs/badge-coverage.svg)



The Video Processing Unit (A.k.a VPU) is the module that process the image from any video source. The proposal is extract some information from the video and provider those data to another system. 

## Architecture 

### Application

This diagram represents a bit of the architecture of how the VPU was built. 

<br/>
<p align="center">
  <img src="imgs/VPU.png">
</p>

> The dashed box (Video) represents a video source outside from the system.

- __A.I. Engine__: This component is responsible to integrate with some framework that will enable other components to run computer vision algorithms (such as object detection).
- __Video Capture__: This component is responsible for integrating with a video source and making sure to always provide the latest frame from the video source.
- __Object Detector or any detector__: This kind of component is responsible for running the specific algorithm and provides the result.
- __Tracked Video__: This component is responsible to aggregate all the algorithm and its status for a specific video source.
- __Main Unit__: This component is responsible to handle all the tracked videos.
- __Websocket__: This component is responsible for integrating with the websocket technology. This component will provide all necessary callbacks to communicate with other systems using websocket.
- __Main Unit + Websocket__: This component is responsible for creating the integration between the main unit and the websocket.

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

To start the VPU, you can do this with following command (run `__main__.py`):

```shell
$ python .
```

## WebSocket Message

- Send video feed ids:
```json
[
  {
    "id": "camera_1",
    "detector_status": "RUNNING"
  },
  {
    "id": "camera_2",
    "detector_status": "ERROR"
  },
]
```

- Send detections:
```json
{
  "id": "camera_1",
  "objects": [
    "car",
    "car",
    "person"
  ]
}
```

- Send error:
```json
{
  "id": "camera_1",
  "error": "Something went wrong"
}
```

- Receive new video feed list:
```json
[
  {
    "id": "camera_1",
    "url": "http://camera.1",
    "config": {
      "run_detection": true
    }
  }
]
```

- Receive to add video feed:
```json
{
  "id": "camera_1",
  "url": "http://camera.1",
  "config": {
    "run_detection": true
  }
}
```

- Receive to remove video feed:
```json
{
  "id": "camera_1"
}
```

- Receive a message to update video config:
```json
{
  "id": "camera_1",
  "config": {
    "run_detection": false
  }
}
```