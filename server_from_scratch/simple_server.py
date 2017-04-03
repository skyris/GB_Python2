import socketserver

HOST, PORT = 'localhost', 9999


class TCPserver(socketserver.TCPServer):
    pass


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("Handled")
        self.data = self.request.recv(1024)
        print(self.data)
        print("End of connection")


server = TCPserver((HOST, PORT), RequestHandler)
print("Server started")
server.serve_forever()
