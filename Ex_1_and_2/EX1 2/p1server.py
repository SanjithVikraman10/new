import socket

def simple_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(1)
    
    print("Server is listening on port 5000...")
    
    connection, address = server_socket.accept()
    print(f"Connection from {address} has been established.")

    client_message = connection.recv(1024).decode('utf-8')
    print(f"Client says: {client_message}")
    
    server_message = "Hello from the server!"
    connection.sendall(server_message.encode('utf-8'))
    
    connection.close()
    server_socket.close()


simple_server()
