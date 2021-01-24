import socket as s
import unittest
from io import BytesIO
from queue import Queue
from unittest.mock import patch

from domain import ResultStruct
from tcp_factory import TCPWorker, SocketFactory, TCPFactory, TCPWorkerFactory


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
                rv = "127.0.0.1" if v[3] == "localhost" else v[3]
                with patch.object(s, "gethostname", return_value=rv):
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


class WorkTest(unittest.TestCase):
    answers = {
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x45\x00"
        b"\x00\x28\x27\x10\x00\x00\xff\x06\x96\xbd\x7f\x00\x00\x01\x7f\x00"
        b"\x00\x01\xb3\xa2\x15\x38\x00\x00\x00\x00\x00\x00\x00\x01\x50\x02"
        b"\x00\x00\xe9\x04\x00\x00":
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x45"
        b"\x00\x00\x2c\x00\x00\x40\x00\x40\x06\x3c\xca\x7f\x00\x00\x01"
        b"\x7f\x00\x00\x01\x15\x38\xb3\xa2\x67\x8e\xc4\x1a\x00\x00\x00"
        b"\x01\x60\x12\xff\xd7\xfe\x20\x00\x00\x02\x04\xff\xd7"
    }

    def setUp(self) -> None:
        resulter = ResultStruct(*ResultStruct.default_config())
        self.factory = TCPWorkerFactory()
        self.factory.set_resulter(resulter)
        timeout, port, queue, seq = 2, 5432, Queue(), 0
        k, host = "127.0.0.1", "127.0.0.1"
        with patch.object(queue, "get", return_value=10000):
            with patch.object(s, "gethostname", return_value=host):
                worker = self.factory.make(timeout, k, host, port, queue, seq)
        self.worker = worker

    @patch("builtins.print")
    @patch("socket.socket.sendto", new_callable=BytesIO)
    def test_work(
        self, mock_print, mock_sendto,
    ):
        for req, res in self.answers.items():
            with patch.object(s.socket, attribute="recv", return_value=res):
                self.worker._work()
                self.assertEqual(req, mock_sendto.get_value())
        self.assertTrue(mock_print.called)


if __name__ == "__main__":
    unittest.main()
