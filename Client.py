import socket
import json
HOST='127.0.0.1'
PORT=6000
NEWLINE = "\r\n"
USERNAME = "bilkentstu"
PASS = "cs421f2022"
ENCODING = "ascii"


class Client:
    def __int__(self):
        pass
    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST,PORT))
            name = f'USER {USERNAME}'
            password = f'PASS {PASS}'
            s.send(bytes(name + NEWLINE, ENCODING))
            s.send(bytes(password + NEWLINE, ENCODING))

            print(s.recv(1024).decode())


            s.close()


cl1 = Client()
cl1.connect()




