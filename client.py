import socket
import threading


class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket):
        threading.Thread.__init__(self)
        self.csocket = client_socket
        print("New connection added: ", client_address)

    def run(self):
        while True:
            data = self.csocket.recv(1024).decode()
            msg = data.decode()
            if msg == 'bye':
                break
            print("from client", msg)
            self.csocket.send(msg)


def client_program():
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    message = input(" -> ")

    while message.lower().strip() != 'exit':
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        cpu_option = client_socket.recv(1024).decode()

        print("CPU's option : " + cpu_option)
        print(str(data))

        message = input(" -> ")

    client_socket.close()


if __name__ == '__main__':
    client_program()
