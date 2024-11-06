import socket
import pickle

class CustomObject:
    def __init__(self, name, value):
        self.name = name
        self.value = value

def enhanced_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    
    print("Server is listening on port 5000...")
    
    connection, address = server_socket.accept()
    print(f"Connection from {address} has been established.")

    # Receive object
    data = connection.recv(4096)
    received_object = pickle.loads(data)
    print(f"Received object: Name = {received_object.name}, Value = {received_object.value}")

    # Send response object
    response_object = CustomObject("ResponseObject", 400)
    connection.sendall(pickle.dumps(response_object))
    
    connection.close()
    server_socket.close()

enhanced_server()
