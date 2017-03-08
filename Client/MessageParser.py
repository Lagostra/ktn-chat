import json
import time

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history,
        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            pass

    def parse_error(self, payload):
        print(tcolors.FAIL + "[ERROR] " + payload['content'] + tcolors.ENDC)

    def parse_info(self, payload):
        self.print_info(payload['content'])

    def print_info(self, info):
        print(tcolors.OKBLUE + "[INFO] " + info + tcolors.ENDC)

    def parse_message(self, payload):
        self.print_message(payload['sender'], payload['content'])

    def print_message(self, sender, msg):
        print(tcolors.OKGREEN + "[" + sender + "] " + tcolors.ENDC + msg)


    def parse_history(self, payload):
        for msg in payload['content']:
            self.print_message('HISTORY', msg)


class tcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__=='__main__':
    MessageParser().parse_info({'content': 'Login successful', 'sender': 'Lagostra'})