import socket
import sys
import time

# HOST = '127.0.0.1'
# PORT = 60000
NEWLINE = "\r\n"
USERNAME = "bilkentstu"
PASS = "cs421f2022"
ENCODING = "ascii"

HOST = sys.argv[1]
PORT = int(sys.argv[2])


class Client:

    def __init__(self, name):
        self.version = 0
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect((HOST, PORT))
        self.OK = 'OK'
        self.INVALID = 'INVALID'
        self.name = name
        self.username = ''
        self.password = ''

    def user_prime(self, name):
        self.name = name

    def user_password(self, pass_user):
        self.password = pass_user

    def kolayGir(self):
        self.name = USERNAME
        self.password = PASS

    def connect(self):
        name = f'USER {self.name}'
        password = f'PASS {self.password}'
        # name = f'USER {USERNAME}'
        # password = f'PASS {PASS}'
        self.s.send(bytes(name + NEWLINE, ENCODING))
        self.s.send(bytes(password + NEWLINE, ENCODING))
        res = self.s.recv(1024).decode()
        print(f'connection status = {res}')
        status, msg = self.receive_response(res)
        if status == self.INVALID:
            quit()

    def update(self):
        cmd = f'UPDT {self.version}'

        res_len = 0
        while res_len <= 5:
            self.s.send(bytes(cmd + NEWLINE, ENCODING))
            response = self.s.recv(1024).decode()
            res_len = len(response)

        status, version, txt = self.receive_update_response(str(response))
        if self.INVALID == status:
            if ('last' in response.strip()):
                print(response)
                return 1
            return -1
        else:
            self.version = int(version)
            with open(f"{self.name}.txt", "w+") as txt_file:
                for line in txt:
                    txt_file.write("".join(line) + "\n")
            print(f"File is updated to version {self.version}. For {self.name}")
            return 1

    def append(self, msg):
        isSuccess = self.update()
        if(isSuccess > 0):
            cmd = f'APND {self.version} {msg}'
            self.s.sendall(bytes(cmd + NEWLINE, ENCODING))
            res = self.s.recv(1024).decode()
            status, splitRes = self.receive_response(res)

            print(splitRes)
            self.version = int(splitRes)

            self.update()
        else:
            print('File was not up to date, It is now updated.')

    def write(self, line, msg):
        isSuccess = self.update()
        if (isSuccess > 0):
            cmd = f'WRTE {self.version} {line} {msg}'
            self.s.send(bytes(cmd + NEWLINE, ENCODING))
            res = self.s.recv(1024).decode()
            status, splitRes = self.receive_response(res)
            self.update()
            print(splitRes)
        else:
            print('File was not up to date, It is now updated.')

    def exit(self):
        self.s.close()

    def receive_response(self, res):
        chunks = res.split(' ')

        print("Response reseived:", chunks)
        return chunks[0], chunks[1]

    def receive_update_response(self, res):
        print(res)
        chunks = res.split(' ')

        status = chunks[0]
        version = chunks[1]
        if status == self.OK and version != '\r\n':
            txt = res[5:len(res) - 1]
            return status, version, txt.split('\n')
        return status, f'{self.version}', []

cl1 = Client('client')

while True:
    print("Please enter the number to choose which protocol you want to proceed with?\n\
          0. CONNECT(enter user and pass before running this)\n\
          1. USER\n\
          2. PASS\n\
          3. WRITE\n\
          4. APPEND\n\
          5. UPDATE\n\
        55. kolay gir\n\
          6. EXIT")

    protocol = int(input())
    if (protocol == 0):
        if (cl1.name == '' or cl1.password == ''):
            print('enter user and password')
        else:
            cl1.connect()
    elif (protocol == 1):
        user_inp = input("Please enter your username.")
        cl1.user_prime(user_inp)
    elif protocol == 2:
        pass_inp = input("Please enter your password.")
        cl1.user_password(pass_inp)
    elif protocol == 3:
        line_num = input("Please enter the line number.")
        message = input("Please enter your message.")
        cl1.write(line_num, message)
    elif protocol == 4:
        app_msg = input("Please enter your message.")
        cl1.append(app_msg)
    elif protocol == 5:
        cl1.update()
    elif protocol == 55:
        cl1.kolayGir()
    elif protocol == 6:
        print("Exiting...")
        cl1.exit()
        break
    else:
        print("Invalid. Please try again.")
