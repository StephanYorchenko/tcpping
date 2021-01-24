import unittest
from queue import Queue
import socket
from unittest.mock import patch

from domain import ResultStruct
from tcp_factory import TCPWorker, SocketFactory, TCPFactory


class WorkerTests(unittest.TestCase):
    data = [
        (2, "127.0.0.1", "127.0.0.1", 5432, 0, "127.0.0.1"),
        (2, "127.0.0.1", "localhost", 5432, 0, "127.0.0.1"),
        (2, "192.168.43.100", "localhost", 5432, 0, "127.0.0.1"),
        (2, "192.168.43.100", "8.8.8.8", 5432, "192.168.43.100"),
    ]

    def setUp(self) -> None:
        self.sockets = SocketFactory()
        self.packets = TCPFactory()
        self.resulter = ResultStruct(*ResultStruct.default_config())
        self.queue = Queue()

    def test_set_source(self):
        with patch.object(self.queue, attribute="get", return_value=23456):
            for v in self.data:
                with patch.object(
                    socket,
                    attribute="gethostname",
                    return_value="127.0.0.1" if v[3] == "localhost" else v[3],
                ):
                    worker = TCPWorker(
                        self.sockets,
                        self.packets,
                        self.resulter,
                        v[0],
                        v[1],
                        v[2],
                        v[3],
                        v[4],
                        self.queue,
                    )
                    self.assertEqual(worker.params[1], v[-1])


if __name__ == "__main__":
    unittest.main()
