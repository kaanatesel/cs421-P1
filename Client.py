import socket
import os
import time

HOST = '127.0.0.1'
PORT = 6000
NEWLINE = "\r\n"
USERNAME = "bilkentstu"
PASS = "cs421f2022"
ENCODING = "ascii"


class Client:

    def __init__(self, name):
        self.version = 0
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.OK = 'OK'
        self.INVALID = 'INVALID'
        self.name = name

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
        data = self.s.recv(1024).decode()
        status, version, txt = self.receive_update_response(data)
        if not data or status != self.OK or version == '-1':
            print("Error while loading txt file.")
        else:
            self.version = int(version)
            with open(f"{self.name}.txt", "w+") as txt_file:
                for line in txt:
                    txt_file.write("".join(line) + "\n")
            print(f"File is updated to version {self.version}. For {self.name}")

    def append(self, msg):
        self.update()
        cmd = f'APND {self.version} {msg}'
        self.s.send(bytes(cmd + NEWLINE, ENCODING))
        res = self.s.recv(1024).decode()
        resEdited = self.receive_response(res)
        print(resEdited)

    def write(self,line, msg):
        self.update()
        cmd = f'WRTE {self.version} {line} {msg}'
        self.s.send(bytes(cmd + NEWLINE, ENCODING))
        res = self.s.recv(1024).decode()
        resEdited = self.receive_response(res)
        print(res)
        print(resEdited)

    def exit(self):
        self.s.close()

    def receive_response(self, res):
        chunks = res.split(' ')

        print("Command received:", chunks)
        return chunks[0], chunks[1]

    def receive_update_response(self, res):
        print(res)
        chunks = res.split(' ')

        status = chunks[0]
        version = chunks[1]
        if status == self.OK and version != '\r\n':
            txt = res[5:len(res) - 1]
            return status, version, txt.split('\n')
        return status, '-1', []


cl1 = Client('kaan')
cl1.append('got')
cl1.append('am')
cl1.append('pipi')
cl1.write('0', 'AMCIII KAAN')
time.sleep(2)
cl1.update()
cl1.exit()

