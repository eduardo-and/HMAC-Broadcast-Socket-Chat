import hmac
import json

from core.constants import *

class Message:
    # type 1: ServerMessage
    # type 2: UserMessage
    def __init__(self, username,):
        self.username=username
        self.type = 2

        
    def send(self,message):
        messageDict ={}
        messageDict["from"]  = self.username
        messageDict["type"]  = self.type
        messageDict["message"]  = message            
        messageDict["digest"]  = self._encrypt(message)            
        return json.dumps(messageDict)
        
    def _encrypt(self,message):
        digest =  hmac.digest(KEY,message.encode('utf-8'),'sha256')
        return digest.hex()
        
        
