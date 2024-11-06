import socket
import pickle

class CustomObject:
    def __init__(self, name, value):
        self.name = name
        self.value = value

def enhanced_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))
    
    # Create and send custom object
    client_object = CustomObject("ClientObject", 42)
    client_socket.sendall(pickle.dumps(client_object))

    # Receive response object
    data = client_socket.recv(4096)
    response_object = pickle.loads(data)
    print(f"Server response: Name = {response_object.name}, Value = {response_object.value}")
    
    client_socket.close()

enhanced_client()
