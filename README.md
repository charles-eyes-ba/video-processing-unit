# Video Processing Unit - VPU

The Video Processing Unit (A.k.a VPU) is the module that run the classification algorithms on the video feeds.

## Application Architecture 
<br/>
<p align="center">
  <img src="imgs/vpu.arch.png">
</p>

## Dependencies

| Module | Version |
| --- | --- |
| [NumPy](https://github.com/numpy/numpy) | 1.21.4 |
| [OpenCV](https://github.com/opencv/opencv-python) | 4.5.4.60 |


## Setup
Create a `.env` file following the `.env.example` file.

## Start
To start the VPU you must install dependencies and run. You can do this with following command

```shell
$ pip install -r requirements.txt
$ python main.py
```