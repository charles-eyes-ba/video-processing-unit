from socketio import ClientNamespace

class ConfigNamespace(ClientNamespace):
    
    REQUEST_UNIT_CONFIGURATION = 'request_unit_configuration'
    
    def __init__(self, namespace=None):
        super().__init__(namespace=namespace)
        self.on_request_unit_configuration_callback = None
        self.on_add_camera_callback = None
        self.on_remove_camera_callback = None
    
    def on_request_unit_configuration(self, data):
        if self.on_request_unit_configuration_callback != None:
            self.on_request_unit_configuration_callback(data)

    def on_add_camera(self, data):
        if self.on_add_camera_callback != None:
            self.on_add_camera_callback(data)

    def on_remove_camera(self, data):
        if self.on_remove_camera_callback != None:
            self.on_remove_camera_callback(data)