import socket

def simple_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))
    
    client_message = "Hello from the client!"
    client_socket.sendall(client_message.encode('utf-8'))

    server_message = client_socket.recv(1024).decode('utf-8')
    print(f"Server says: {server_message}")
    
    client_socket.close()

simple_client()
    