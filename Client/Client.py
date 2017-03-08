# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.host = host
        self.server_port = server_port
        self.message_parser = MessageParser()

        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        self.message_receiver = MessageReceiver(self, self.connection)
        self.message_parser.print_info('Connected to server')
        
    def disconnect(self):
        self.message_parser.print_info('Disconnected from server.')

    def receive_message(self, message):
        self.message_parser.parse(message)

    def send_payload(self, data):
        self.connection.send(data)

    def send(self, request, content = ''):
        msg = json.dumps({
            'request': request,
            'content': content
        })
        self.send_payload(msg.encode("utf-8"))

    def help(self):
        self.send('help')

    def history(self):
        self.send('history')

    def login(self, username):
        self.send('login', username)

    def logout(self):
        self.send('logout')

    def list_chatrooms(self):
        self.send('chatrooms')

    def list_names(self):
        self.send('names')

    def send_message(self, message):
        self.send('msg', message)

    def send_message_to(self, message, username):
        msg = json.dumps({
            'request': 'direct_msg',
            'content': message,
            'recipient': username
        })
        self.send_payload(msg.encode("utf-8"))

    def create(self, chatroom):
        self.send('create', chatroom)

    def join(self, chatroom):
        self.send('join', chatroom)


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
