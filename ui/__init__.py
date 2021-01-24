import argparse
import signal
import socket
import sys

from domain import Message
from domain.manager import Manager


class CLInterface:
    def __init__(self, manager):
        self.manager = manager

    @staticmethod
    def get_input_parameters():
        parser = argparse.ArgumentParser(
            description="Утилита для проверки целостности и качества"
            " соединений в сетях на основе TCP/IP"
        )
        parser.add_argument("host", type=str, help="host of server")
        parser.add_argument("port", type=int, help="target port")
        parser.add_argument(
            "--max-count",
            type=int,
            default=100,
            help="maximum count of requests DEFAULT: 100",
        )
        parser.add_argument(
            "--nseconds",
            type=int,
            default=1,
            help="count seconds between sending requests DEFAULT: 1",
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=2,
            help="maximum seconds for waiting server receive DEFAULT: 2",
        )
        return parser.parse_args()

    def run(self):
        signal.signal(signal.SIGINT, self.sigint_handler)
        signal.signal(signal.SIGUSR1, self.usr1_handler)
        self.manager.start()
        self.manager.join()
        CLInterface.show(self.manager.result_struct)

    @staticmethod
    def start(worker_factory, result_struct):
        input_args = CLInterface.get_input_parameters()
        input_args.src = socket.gethostbyname(socket.gethostname())
        manager = Manager(worker_factory, result_struct, input_args)
        return CLInterface(manager)

    def usr1_handler(self, signal, frame):
        CLInterface.show(self.manager.result_struct)

    @staticmethod
    def show(row) -> None:
        print(row)

    def sigint_handler(self, signal, frame):
        CLInterface.show(self.manager.result_struct)
        self.manager.is_stopped = True
        sys.exit(0)

    @staticmethod
    def catch_error(message: Message):
        CLInterface.show(message)
        sys.exit(message.value)
