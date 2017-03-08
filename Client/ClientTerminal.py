from Client import Client
import shlex

class ClientTerminal:

    commands = {}
    client = None

    def __init__(self):
        self.commands = {
            'chatroom': self.handle_chatroom,
            'connect': self.handle_connect,
            'help': self.handle_help,
            'help_raw': self.handle_help_raw,
            'history': self.handle_history,
            'login': self.handle_login,
            'logout': self.handle_logout,
            'names': self.handle_names,
            'send': self.handle_send,
            'send_raw': self.handle_send_raw
        }

    def run(self):
        print()
        print('Welcome to the Chatinator mk IV!')
        print('Enter command below')
        print('Enter \'help\' for a list of available commands\r\n')
        command = input("")
        while command != "exit":
            if command:
                lst = shlex.split(command)

                if lst[0] in self.commands:
                    if self.client == None and lst[0] != 'help' and lst[0] != 'connect':
                        print("You must connect before you interact with the server.")
                    else:
                        self.commands[lst[0]](lst[1:])
                else:
                    print('Invalid command')

            command = input("")

        if self.client != None:
            self.client.logout()

    def handle_chatroom(self, params):
        if params[0] == 'create':
            self.client.create(params[1])
        elif params[0] == 'join':
            self.client.join(params[1])
        elif params[0] == 'list':
            self.client.list_chatrooms()
        else:
            print("Invalid command")

    def handle_connect(self, params): # Connect <host>:<port>
        if self.client != None:
            self.client.logout()

        addr = params[0].split(":")
        self.client = Client(addr[0], int(addr[1]))

    def handle_help(self, params):
        print('These are the available commands:\r\n')
        cmds = [
            ('chatroom create <chatroom_name>', 'Create a chatroom with name <chatroom_name> if it does not exist'),
            ('chatroom join <chatroom_name>', 'Attempt to join a chatroom with name <chatroom_name>'),
            ('connect <host>:<port>', 'Attempts to connect to a server running on port <port> on host <host>'),
            ('exit', 'Exit the program'),
            ('help', 'Shows this help menu'),
            ('help_raw', 'Get all supported request types from the server'),
            ('history', 'Get all previous messages in current chatroom'),
            ('login <username>', 'Log in to currently connected server with username <username>'),
            ('logout', 'Log out and disconnect from server'),
            ('names', 'List all users in current chatroom'),
            ('send <msg> [user_id]', 'Send a message to current chatroom, or to [user_id] if specified'),
            ('send_raw <request> <content>', '')
        ]

        width = len(max(cmds, key=lambda x: len(x[0]))[0])
        for cmd in cmds:
            print('{:{width}}\t\t{}'.format(cmd[0], cmd[1], width=width))

    def handle_help_raw(self, params):
        self.client.help()

    def handle_history(self, params):
        self.client.history()

    def handle_login(self, params):
        self.client.login(params[0])

    def handle_logout(self, params):
        self.client.logout()

    def handle_names(self, params):
        self.client.list_names()

    def handle_send(self, params): # send <msg> [user_id]
        if len(params) > 1:
            self.client.send_message_to(params[0], params[1])
        else:
            self.client.send_message(params[0])

    def handle_send_raw(self, params):
        param2 = "" if len(params) < 2 else params[1]
        self.client.send(params[0], param2)


if __name__=='__main__':
    ClientTerminal().run()