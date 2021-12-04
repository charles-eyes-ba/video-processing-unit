from socketio import ClientNamespace

class ConfigNamespace(ClientNamespace):
    def on_request_unit_configuration(self, data):
        print('on_request_unit_configuration', data)

    def on_add_camera(self, data):
        print('on_add_camera', data)

    def on_remove_camera(self, data):
        print('on_remove_camera', data)

    