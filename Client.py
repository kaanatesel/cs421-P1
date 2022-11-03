import socket
import io

HOST = '127.0.0.1'
PORT = 6000
NEWLINE = "\r\n"
USERNAME = "bilkentstu"
PASS = "cs421f2022"
ENCODING = "ascii"


class Client:

    def __init__(self):
        self.version = 3
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.OK = 'OK'
        self.INVALID = 'INVALID'

    def connect(self):
        self.s.connect((HOST, PORT))
        name = f'USER {USERNAME}'
        password = f'PASS {PASS}'
        self.s.send(bytes(name + NEWLINE, ENCODING))
        self.s.send(bytes(password + NEWLINE, ENCODING))
        print(f'connection status = {self.s.recv(1024).decode()}')

    def update(self):
        cmd = f'UPDT {self.version}'
        self.s.send(bytes(cmd + NEWLINE, ENCODING))
        response = self.s.recv(1024).decode()
        status, message = self.receive_response(response)
        if(status == self.OK):
            self.version = int(message)
        else:
            print("ERROR, cannot update")

    def write(self):
        pass

    def exit(self):
        self.s.close()

    def receive_response(self, res):
        chunks = res.split(' ')

        print("Command received:", chunks)
        return chunks[0], chunks[1]


cl1 = Client()
cl1.update()
