# -*- coding: utf-8 -*-
import socketserver
import socket
import json
import re
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

chatrooms = {'default': {}}
history = {'default': []}
users = {}

def send_to_chatroom(chatroom, sender, response, content):
    for username, user in chatrooms[chatroom].items():
        msg = user.send(sender, response, content)
    return msg
	
def send_to_user(username, sender, response, content):
    users[username].send(sender, response, content)

class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    chatroom = 'default'
    username = None

    def handle(self):
        possible_requests = {
            'create': self.handle_create,
            'direct_msg': self.handle_direct_msg,
            'help': self.handle_help,
            'history': self.handle_history,
            'join': self.handle_join,
            'chatrooms': self.handle_chatrooms,
            'login': self.handle_login,
            'logout': self.handle_logout,
            'msg': self.handle_msg,
            'names': self.handle_names,
        }

        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096).decode("utf-8")
            if len(received_string) > 0:
                payload = json.loads(received_string)

                if payload['request'] in possible_requests:
                    if self.username == None and payload['request'] != 'login' and payload['request'] != 'help':
                        self.send_error('Login before you do anything else...')
                    else:
                        possible_requests[payload['request']](payload)
                else:
                    pass

    def handle_create(self, payload):
        if self.username == None:
            self.send_error('You must login before you can create a chatroom')
        elif payload['content'] in chatrooms:
            self.send_error('Chatroom \'' + payload['content'] + '\' already exists')
        else:
            chatrooms[payload['content']] = {}
            history[payload['content']] = []
            self.send_info('Chatroom \'' + payload['content'] + '\' created successfully. You can now join it.')

    def handle_chatrooms(self, payload):
        names = ", ".join(chatrooms.keys())
        self.send_info('Available chatrooms: ' + names)

    def handle_direct_msg(self, payload):
        if payload['recipient'] in users:
            send_to_user(payload['recipient'], self.username, 'message', payload['content'])
        else:
            self.send_error('No user with username \'' + payload['recipient'] + '\' connected')

    def handle_help(self, payload):
        cmds = [
            ('create <chatroom>', 'Create a chatroom with name <chatroom>'),
            ('help', 'Return this help text'),
            ('history', 'Get all messages sent in the current chatroom'),
            ('join <chatroom>', 'Join the chatroom with name <chatroom>'),
            ('chatrooms', 'List all available chatrooms'),
            ('login <username','Log in with username <username>'),
            ('logout', 'Log out and disconnect from server'),
            ('msg <message>', 'Send a message to all users in current chatroom'),
            ('names', 'List all users in current chatroom'),
        ]

        string = "Available requests:"
        width = len(max(cmds, key=lambda x: len(x[0]))[0])
        for cmd in cmds:
            string += '\r\n{:{width}}\t\t{}'.format(cmd[0], cmd[1], width=width)

        self.send_info(string)

    def handle_history(self, payload = None):
        if len(history[self.chatroom]) > 0:
            self.send('SERVER', 'history', history[self.chatroom])

    def handle_join(self, payload):
        if self.username == None:
            self.send_error('You must login before you can join a chatroom')
        elif payload['content'] in chatrooms:
            del chatrooms[self.chatroom][self.username]
            self.chatroom = payload['content']
            chatrooms[self.chatroom][self.username] = self
            send_to_chatroom(self.chatroom, 'SERVER', 'info', 'User ' + self.username +
                             " joined the chatroom (" + self.chatroom + ")")
            time.sleep(0.5)
            self.handle_history()
        else:
            self.send_error('Chatroom \'' + payload['content'] + '\' does not exist')

    def handle_login(self, payload):
        if self.username == None:
            if not self.is_valid_username(payload['content']):
                self.send_error('Username may only contain alphanumeric characters')
                return
            elif len(payload['content']) < 3 or len(payload['content']) > 15:
                self.send_error('Username must be between 3 and 15 characters')
                return
            elif payload['content'] in users:
                self.send_error('Username already taken')
                return

            self.username = payload['content']
            self.chatroom = 'default'
            users[self.username] = self
            chatrooms[self.chatroom][self.username] = self
            self.send_info('Logged in successfully')
            time.sleep(0.5)
            self.handle_history()

    def handle_logout(self, payload):
        del users[self.username]
        del chatrooms[self.chatroom][self.username]
        self.send_info("Logged out successfully")
        self.connection.shutdown(socket.SHUT_RDWR)

    def handle_msg(self, payload):
        msg = send_to_chatroom(self.chatroom, self.username, 'message', payload['content'])
        history[self.chatroom].append(msg)

    def handle_names(self, payload):
        names = ", ".join(chatrooms[self.chatroom].keys())
        self.send_info('Users in current chatroom: ' + names)

    def is_valid_username(self, username):
        return re.match('[a-zA-Z0-9]+', username)

    def send_info(self, content):
        self.send('SERVER', 'info', content)

    def send_error(self, content):
        self.send('SERVER', 'error', content)

    def send(self, sender, response, content):
        msg = json.dumps({
            'timestamp': time.time(),
            'sender': sender,
            'response': response,
            'content': content
        })

        self.connection.send(msg.encode("utf-8"))
        return msg


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = '0.0.0.0', 9998
    print ('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
