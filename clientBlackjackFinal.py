import socket
# Obtains Server IP address and Port Number
serverName = '10.220.25.180' #socket.gethostname()
serverPort = 5000
sentence = input('Type "play" To Start Game ')

# Loop that sends data to server
while True:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(sentence.encode())
    game = clientSocket.recv(1024)
    print(game.decode())
    # If the data from the server contains "Game Over" client closes
    if "Game Over" in game.decode():
        clientSocket.close()
        break
    sentence = input()

clientSocket.close()