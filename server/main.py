import socket
import threading
from models.client import * 
from models.message import * 
from core.constants import * 

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
print(f'Servidor iniciado em: {HOST}:{PORT}')

clients = []
msg = Message()

def globalMessage(message):
    for client in clients:
        client.connection.send(message)

def handleMessages(client):
    while True:
        try:
            receiveMessageFromClient = client.connection.recv(2048).decode('utf-8')
            globalMessage(receiveMessageFromClient.encode('utf-8'))
        except:
            clientLeaved = clients.index(client)
            client.connection.close()
            clients.remove(clients[clientLeaved])
            clientLeavedUsername = client.username
            print(msg.send(f'{clientLeavedUsername} se desconectou...'))
            globalMessage(msg(f'{clientLeavedUsername} saiu...'.encode('utf-8')))    


def initialConnection():
    while True:
        try:
            connection, address = server.accept()
            print(f"Nova conexão: {str(address)}")
            connection.send(msg.send('getUser').encode('utf-8'))
            username = connection.recv(2048).decode('utf-8')
            client = Client(connection,username)
            clients.append(client)
            globalMessage(msg.send(f'{username} Entrou no chat!').encode('utf-8'))
            user_thread = threading.Thread(target=handleMessages,args=(client,))
            user_thread.start()
        except:
            pass

initialConnection()