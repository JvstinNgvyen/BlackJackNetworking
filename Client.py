# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 13:03:08 2018

@author: Salem Othman
"""
import socket
serverName = socket.gethostname()
serverPort = 5000

sentence = input('Input lowercase sentence:')
while (sentence!='exit'):
    data = clientSocket.recv(1024).decode()
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024)
    print ('From Server:', modifiedSentence.decode())
    clientSocket.close()
    sentence = input('Input lowercase sentence:')


