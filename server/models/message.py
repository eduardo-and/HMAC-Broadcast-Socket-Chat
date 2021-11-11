import hmac
import json


class Message:
    # type 1: ServerMessage
    # type 2: UserMessage
    def __init__(self, username="Server"):
        self.username = username

    def send(self, message):
        messageDict = {}
        messageDict["from"] = self.username
        messageDict["type"] = 1
        messageDict["digest"] = ''
        messageDict["message"] = message
        return json.dumps(messageDict)
