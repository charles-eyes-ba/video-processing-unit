from src.external.deep_neural_network.dnn_opencv import DNNOpenCV

def create_dnn(config_path, weights_path, classes_path):
    return DNNOpenCV(config_path, weights_path, classes_path)