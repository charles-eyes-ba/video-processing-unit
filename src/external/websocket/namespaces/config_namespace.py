from socketio import ClientNamespace
from src.common.call import call

class ConfigNamespace(ClientNamespace):
    """ Class that handles the /config namespace """
    
    REQUEST_UNIT_CONFIGURATION = 'request_unit_configuration'
    
    def __init__(self):
        super().__init__(namespace='/config')
        self.on_request_unit_configuration_callback = None
        self.on_add_camera_callback = None
        self.on_remove_camera_callback = None
        
    
    def setup_callbacks(self, on_request_unit_configuration=None, on_add_camera=None, on_remove_camera=None):
        """
        Setup the callbacks
        
        Parameters
        ----------
        on_request_unit_configuration : function
            Callback for the request_unit_configuration event
        on_add_camera : function
            Callback for the add_camera event
        on_remove_camera : function
            Callback for the remove_camera event
        """
        self.on_request_unit_configuration_callback = on_request_unit_configuration
        self.on_add_camera_callback = on_add_camera
        self.on_remove_camera_callback = on_remove_camera
    
    
    def on_request_unit_configuration(self, data):
        """ Callback for the request_unit_configuration event """
        call(self.on_request_unit_configuration_callback, data)


    def on_add_camera(self, data):
        """ Callback for the add_camera event """
        call(self.on_add_camera_callback, data)
        

    def on_remove_camera(self, data):
        """ Callback for the remove_camera event """
        call(self.on_remove_camera_callback, data)