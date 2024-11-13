import socket

# Function to print the board state
def print_board(board):
    print(f"  {board[12]} {board[11]} {board[10]} {board[9]} {board[8]} {board[7]}")
    print(f"{board[13]}            {board[6]}")
    print(f"  {board[0]} {board[1]} {board[2]} {board[3]} {board[4]} {board[5]}")

# Initialize the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("127.0.0.1", 5912)

print("Mancala client is running...")

msgtoServer = input("Send a message to Server: ") #Message to be sent to server.
client_socket.sendto(msgtoServer.encode(), server_address) #Message sent to server.

#Waiting to receive response from Server..
data, content = client_socket.recvfrom(1024);
msgfromServer = data.decode()
print("Message from Server:", msgfromServer)

#Waiting to load up game from Server..
print()
data, content = client_socket.recvfrom(1024);
msgfromServer = data.decode()
print("Message from Server:", msgfromServer)

#Reply Server to Load game or not..
rtoServer = input(msgfromServer+" : ")
client_socket.sendto(rtoServer.encode(), server_address)

if rtoServer.lower() == "y":
    while True:
        move = input("Enter your move (0-5 for player 1, 7-12 for player 2): ")
        client_socket.sendto(move.encode(), server_address)
        data, _ = client_socket.recvfrom(1024)

        if data.decode() == "Invalid move":
            print("Invalid move. Try again.")
        else:
            board = eval(data.decode())
            print_board(board)
else:
    print("You refused to play game.")

client_socket.close()
