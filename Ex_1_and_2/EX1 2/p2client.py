import Pyro4

def rmi_client():
    # Locate the RMI server by the name 'example.rmi'
    remote_service = Pyro4.Proxy("PYRONAME:example.rmi")
    
    # Call the remote method
    response = remote_service.say_hello("Client")
    print(f"Server says: {response}")

if __name__ == "__main__":
    rmi_client()