import Pyro4

# Create a class for the remote service
@Pyro4.expose
class RemoteService:
    def say_hello(self, name):
        return f"Hello, {name}! This is the RMI server."

# Start the Pyro4 Daemon with the service
def start_server():
    # Pyro4 Daemon setup
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()  # Locate the name server
    uri = daemon.register(RemoteService)  # Register the service
    ns.register("example.rmi", uri)  # Register the service with a name in the name server

    print(f"RMI Server started with URI: {uri}")
    daemon.requestLoop()  # Start the event loop for listening

# Uncomment the following line to start the server
start_server()
