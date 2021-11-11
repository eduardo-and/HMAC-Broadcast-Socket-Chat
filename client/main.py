from json import *
import socket
import threading
from core.constants import *
from models.message import *

ServerIP = HOST
_PORT = PORT

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    username = input('Enter a username: ')
    server.connect((ServerIP, _PORT))
    print(f'Conectado em {ServerIP}:{_PORT}')
    msg = Message(username)
except:
    print(f'ERROR: Check a entrada: {ServerIP}:{_PORT}')


def jsonDecoder(value):
    newValue = json.loads(value)
    return newValue["type"], newValue["message"], newValue["digest"], newValue["from"]

def receiveMessage():
    while True:
        try:
            message = server.recv(2048).decode('utf-8')
            type, content, digest, sender = jsonDecoder(message)
            if content == 'getUser' and type == 1:
                server.send(username.encode('utf-8'))
            elif(type == 2):
                if(verifyIntegrity(content, digest)):
                    if(sender != username):
                        print(f'{sender}:  {content}')
                    continue
                else:
                    print(f'{sender}:  Mensagem possívelmente adulterada! ')
            else:
                print(f'{content}')
        except:
            print('ERROR: Check your connection or server might be offline')


def sendMessage():
    while True:
        message = input()
        server.send(msg.send(message).encode('utf-8'))


thread1 = threading.Thread(target=receiveMessage, args=())
thread2 = threading.Thread(target=sendMessage, args=())

thread1.start()
thread2.start()


def verifyIntegrity(message, hash):
    newHmac = hmac.digest(KEY, message.encode('utf-8'), 'sha256')
    return hmac.compare_digest(hash.encode('utf-8'), newHmac.hex().encode('utf-8'))

