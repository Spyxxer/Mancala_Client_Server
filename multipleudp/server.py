import socket

# Define the initial state of the Mancala board
def init_board():
    return [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

# Function to handle the player's move
def make_move(board, pit, player):
    if board[pit] == 0 or pit in [6, 13]:
        return False, board
    
    stones = board[pit]
    board[pit] = 0
    index = pit

    while stones > 0:
        index = (index + 1) % 14
        if (player == 0 and index == 13) or (player == 1 and index == 6):
            continue
        board[index] += 1
        stones -= 1

    return True, board

# Function to check if the game is over
def game_over(board):
    return sum(board[:6]) == 0 or sum(board[7:13]) == 0

# Function to print the board state
def print_board(board):
    print(f"  {board[12]} {board[11]} {board[10]} {board[9]} {board[8]} {board[7]}")
    print(f"{board[13]}             {board[6]}")
    print(f"  {board[0]} {board[1]} {board[2]} {board[3]} {board[4]} {board[5]}")

# Initialize the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("127.0.0.1", 5712))

board = init_board()
player_turn = 0

print("Mancala server is running...")

clients = {}

while not game_over(board):
    data, addr = server_socket.recvfrom(1024);
    cclient = clients.get(addr[1], False)
    if cclient:
        move = int(data.decode())
        if (player_turn == 0 and 0 <= move <= 5) or (player_turn == 1 and 7 <= move <= 12):
            valid, board = make_move(board, move, player_turn)
            if valid:
                player_turn = 1 - player_turn
            server_socket.sendto(str(board).encode(), addr)
            print_board(board)
            print("-------------------------------------------------------")
            print("First Player's Turn." if player_turn == 0 else "Second Player's Turn.")
            print("-------------------------------------------------------")
        else:
            server_socket.sendto(b"Invalid move", addr)
    else:
        clients[addr[1]] = False #Setting client greeting to False
        print("Existing Clients:", clients);
        msgfromClient = data.decode();
        print(f"Message from Client: {msgfromClient}")
        msgToClient = input("Send Message to Client: "); server_socket.sendto(msgToClient.encode(), addr)
        qStart = "Do you want to play, reply with (y/n)"
        server_socket.sendto(qStart.encode(), addr)

        #Loading response from Client.
        rdata, raddr = server_socket.recvfrom(1024)
        rfromClient = rdata.decode(); 
        if rfromClient == 'y':
            clients[addr[1]] = True
            print("---------------------------------------------------------")
        else:
            print("Client declined to play game!"); break
print("Game over.")
