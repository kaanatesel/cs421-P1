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

    def __init__(self):
        self.version = 0

        #self.user_prime(nickname)
        self.OK = 'OK'
        self.INVALID = 'INVALID'
        #self.name = name

    def user_prime(self, nickname):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))
        cmd = f'USER {USERNAME} {nickname}'
        self.s.send(bytes(nickname + NEWLINE, ENCODING))
        print(f'connection status = {self.s.recv(1024).decode()}')  # ne yazdırcaz emin olamadım

    def password(self, pass_user):
        self.s.connect((HOST, PORT))
        password = f'PASS {PASS}{pass_user}'
        self.s.send(bytes(password + NEWLINE, ENCODING))
        print(f'connection status = {self.s.recv(1024).decode()}')#ne yazdırcaz emin olamadım

    def update(self):
        cmd = f'UPDT {self.version}\r\n'
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
        cmd = f'APND {self.version} {msg}\r\n'
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
        cmd = f'EXIT \r\n'
        self.s.send(bytes(cmd + NEWLINE, ENCODING))
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


cl1 = Client()
##cl1.append('irem')
##cl1.append('ekin')
##cl1.append('atei')
##cl1.write('0', 'KAAN KAAN KAAN')
##time.sleep(2)
##cl1.update()
##cl1.exit()

print("Please enter the number to choose which protocol you want to proceed with?\n\
      1. USER\n\
      2. PASS\n\
      3. WRITE\n\
      4. APPEND\n\
      5. UPDATE\n\
      6. EXIT")

protocol = int(input())

if (protocol == 1):
    user_inp = input("Please enter your username.")
    cl1.user_prime(user_inp)

elif protocol == 2:
    pass_inp = input ("Please enter your password.")
    cl1.password(pass_inp)

elif protocol == 3:
    line_num= input ("Please enter the line number.")
    message = input("Please enter your message.")
    cl1.write(line_num, message)
elif protocol == 4:
    app_msg= input ("Please enter your message.")
    cl1.append(app_msg)
elif protocol == 5:
    cl1.update()
    print("The server is updated.")
elif protocol == 6:
    print("Exiting...")
    cl1.exit()
else:
    print("Invalid. Please try again.")