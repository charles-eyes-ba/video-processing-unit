from socketio import ClientNamespace

class ConfigNamespace(ClientNamespace):
    """ Class that handles the /config namespace """
    
    REQUEST_UNIT_CONFIGURATION = 'request_unit_configuration'
    
    def __init__(self):
        super().__init__(namespace='/config')
        self.on_request_unit_configuration_callback = None
        self.on_add_camera_callback = None
        self.on_remove_camera_callback = None
    
    def on_request_unit_configuration(self, data):
        """ Callback for the request_unit_configuration event """
        if self.on_request_unit_configuration_callback != None:
            self.on_request_unit_configuration_callback(data)

    def on_add_camera(self, data):
        """ Callback for the add_camera event """
        if self.on_add_camera_callback != None:
            self.on_add_camera_callback(data)

    def on_remove_camera(self, data):
        """ Callback for the remove_camera event """
        if self.on_remove_camera_callback != None:
            self.on_remove_camera_callback(data)