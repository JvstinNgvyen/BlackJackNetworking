# -*- coding: utf-8 -*-
import socket

serverName = socket.gethostname()
serverPort = 5000
complete_info = ''
sentence = input('Type "play" to start game ')
while sentence != 'exit':

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(sentence.encode())
    game = clientSocket.recv(1024)
    print(game.decode())
    clientSocket.close()
    sentence = input()