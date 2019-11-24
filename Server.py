# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 13:00:46 2018

@author: Salem Othman
"""
import socket






serverPort = 5000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()
