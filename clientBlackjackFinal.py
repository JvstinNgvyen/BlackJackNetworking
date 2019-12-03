# -*- coding: utf-8 -*-
import socket

serverName = '192.168.0.4' #socket.gethostname()
serverPort = 5000
sentence = input('Type "play" To Start Game ')

while True:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(sentence.encode())
    game = clientSocket.recv(1024)
    print(game.decode())

    if "Game Over" in game.decode():
        clientSocket.close()
        break
    sentence = input()

clientSocket.close()