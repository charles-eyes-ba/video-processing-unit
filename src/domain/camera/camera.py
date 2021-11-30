class Camera:
    """ Class that contains the camera and its algorithms """
    def __init__(self, id, cam):
        self.id = id
        self.cam = cam

    def pop_lastest_frame(self):
        return self.cam.pop_lastest_frame()