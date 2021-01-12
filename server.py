import socket
import random
import threading

number_clients = 0
in_game = 0
win = 0
lose = 0


class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket):
        global number_clients
        threading.Thread.__init__(self)
        self.csocket = client_socket
        number_clients = number_clients + 1
        self.number = number_clients
        print("New connection added: ", client_address)

    def run(self):
        global number_clients
        global in_game
        global win
        global lose

        while win == 0:
            if in_game == 0:
                self.csocket.send("Your turn".encode())
                in_game = 1
                while True:
                    data = self.csocket.recv(1024).decode()
                    if not data:
                        break
                    print("User's option: " + str(data))

                    option_number = random.randrange(0, 4)

                    print("CPU's option: " + options[option_number])

                    if str(data) == "rock" or str(data) == "Rock":
                        result = check_win_rock(options[option_number])
                    elif str(data) == "paper" or str(data) == "Paper":
                        result = check_win_paper(options[option_number])
                    elif str(data) == "scissors" or str(data) == "Scissors":
                        result = check_win_scissors(options[option_number])
                    elif str(data) == "lizard" or str(data) == "Lizard":
                        result = check_win_lizard(options[option_number])
                    elif str(data) == "spock" or str(data) == "Spock":
                        result = check_win_spock(options[option_number])
                    else:
                        result = "This option is unavailable"

                    self.csocket.send(result.encode())
                    self.csocket.send(options[option_number].encode())

                    if result == "You lose":
                        in_game = 0
                        lose += 1
                        break
                    elif result == "You win":
                        win = 1
                        break

        self.csocket.close()


options = ["rock", "paper", "scissors", "lizard", "spock"]


def check_win_rock(option):
    if option == "scissors" or option == "lizard":
        return "You win"
    elif option == "paper" or option == "spock":
        return "You lose"
    elif option == "rock":
        return "Draw"


def check_win_paper(option):
    if option == "spock" or option == "rock":
        return "You win"
    elif option == "lizard" or option == "scissors":
        return "You lose"
    elif option == "paper":
        return "Draw"


def check_win_scissors(option):
    if option == "paper" or option == "lizard":
        return "You win"
    elif option == "rock" or option == "spock":
        return "You lose"
    elif option == "scissors":
        return "Draw"


def check_win_lizard(option):
    if option == "spock" or option == "paper":
        return "You win"
    elif option == "scissors" or option == "rock":
        return "You lose"
    elif option == "lizard":
        return "Draw"


def check_win_spock(option):
    if option == "scissors" or option == "rock":
        return "You win"
    elif option == "paper" or option == "lizard":
        return "You lose"
    elif option == "spock":
        return "Draw"


threads = []


def server_program():
    global number_clients
    global in_game
    global win
    global lose

    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()

    server_socket.bind((host, port))

    while True:
        server_socket.listen(3)
        conn, address = server_socket.accept()

        if number_clients < 3:
            print("Connection from: " + str(address))

            new_thread = ClientThread(address, conn)
            threads.append(new_thread)
            new_thread.start()
        elif win == 0:
            print("Maximum number of clients reached")
            conn.send("Maximum number of clients reached".encode())

            conn.close()

        message = input(" -> ")
        if message == "Reset":
            number_clients = 0
            win = 0
            lose = 0
            in_game = 0


if __name__ == '__main__':
    server_program()
