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
while True:
    overview = ''
    start_time = datetime.now()

    for camera in [camera_1, camera_2, camera_3, camera_4]:
        frame = camera.pop_lastest_frame()

        if frame is not None:
            boxes, scores, classes = yolo.predict(frame)
            overview += f'Camera: {camera.id} {classes}\n'

    overview += f'Time to process: {datetime.now() - start_time}\n'
    overview += f'Stated time: {start_time}\n'
    print(overview)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```
