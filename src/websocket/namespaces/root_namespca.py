from socketio import ClientNamespace

class RootNamespace(ClientNamespace):
    def on_connect(self):
        print('connected to server')

    def on_disconnect(self):
        print('disconnected from server')

    def on_reconnect(self):
        print('reconnected to server')