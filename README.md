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
