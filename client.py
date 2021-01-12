import socket


def client_program():
    message = ""
    host = socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    turn = client_socket.recv(1024).decode()

    if turn == "Your turn":
        print("Your turn")
        message = input(" -> ")
    elif turn == "Maximum number of clients reached":
        print("Maximum number of clients reached")
        turn = "OUT"
    elif turn == "The game is over":
        print("The game is over")
        turn = "OUT"

    while message.lower().strip() != 'exit' and turn != "OUT":
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        cpu_option = client_socket.recv(1024).decode()

        print("CPU's option : " + cpu_option)
        print(str(data))

        if data == "You win" or data == "You lose":
            break
        else:
            print("Try again")

        message = input(" -> ")

    client_socket.close()


if __name__ == '__main__':
    client_program()
