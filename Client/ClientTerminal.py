#from Client import Client

class ClientTerminal:

    commands = {}
    client = None

    def __init__(self):
        self.commands = {
            'chatroom': self.handle_chatroom,
            'connect': self.handle_connect,
            'help': self.handle_help,
            'history': self.handle_history,
            'send': self.handle_send,
        }

    def run(self):
        print('Welcome to the Chatinator mk IV!')
        print('Enter command below')
        print('Enter \'help\' for a list of available commands\r\n')
        command = input(">> ")
        while command != "exit":
            lst = command.split(" ")
            try:
                self.commands[lst[0]](lst[1:])
            except KeyError:
                print('Invalid command')

            command = input(">> ")

        if self.client != None:
            self.client.disconnect()


    def handle_chatroom(self, params):
        if params[0] == 'create':
            pass
        elif params[0] == 'join':
            pass
        else:
            print("Invalid command")


    def handle_help(self, params):
        print('These are the available commands:\r\n')
        cmds = [
            ('chatroom create <chatroom_name>', 'Create a chatroom with name <chatroom_name> if it does not exist'),
            ('chatroom join <chatroom_name>', 'Attempt to join a chatroom with name <chatroom_name>'),
            ('connect <host>:<port>', 'Attempts to connect to a server running on port <port> on host <host>'),
            ('help', 'Shows this help menu'),
            ('history', 'Get all previous messages in current chatroom'),
            ('send <msg> [user_id]', 'Send a message to current chatroom, or to [user_id] if specified')
        ]

        width = len(max(cmds, key=lambda x: len(x[0]))[0])
        for cmd in cmds:
            print('{:{width}}\t\t{}'.format(cmd[0], cmd[1], width=width))


    def handle_history(self, params):
        pass

    def handle_connect(self, params): # Connect <host>:<port>
        if self.client != None:
            self.client.disconnect()

        addr = params[0].split(":")
        self.client = Client(addr[0], addr[1])


    def handle_send(self, params): # send <msg> [user_id]
        pass


if __name__=='__main__':
    ClientTerminal().run()