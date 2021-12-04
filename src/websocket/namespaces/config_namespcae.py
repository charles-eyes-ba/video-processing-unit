from socketio import ClientNamespace

class ConfigNamespace(ClientNamespace):
    
    REQUEST_UNIT_CONFIGURATION = 'request_unit_configuration'
    
    def on_request_unit_configuration(self, data):
        print('on_request_unit_configuration')

    def on_add_camera(self, data):
        print('on_add_camera', data)

    def on_remove_camera(self, data):
        print('on_remove_camera', data)

    