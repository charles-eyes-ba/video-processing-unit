from socketio import ClientNamespace

class DetectionNamespace(ClientNamespace):
    """ Class that handles the /detection namespace """
    DETECT = 'detect'
    
    def __init__(self):
        super().__init__(namespace='/detection')