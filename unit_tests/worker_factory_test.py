import socket as s
import unittest
from queue import Queue
from unittest.mock import patch

from domain import ResultStruct
from tcp_factory import TCPWorkerFactory, TCPFactory, SocketFactory


class WorkerFactoryTest(unittest.TestCase):
    def setUp(self) -> None:
        resulter = ResultStruct(*ResultStruct.default_config())
        self.factory = TCPWorkerFactory()
        self.factory.set_resulter(resulter)

    def test_make(self):
        timeout, port, queue, seq = 2, 5432, Queue(), 0
        k, host = "127.0.0.1", "8.8.8.8"
        with patch.object(queue, attribute="get", return_value=23456):
            with patch.object(s, attribute="gethostname", return_value=host):
                worker = self.factory.make(timeout, k, host, port, queue, seq)
        self.assertIsInstance(worker.resulter, ResultStruct)
        self.assertIsInstance(worker.pack_factory, TCPFactory)
        self.assertIsInstance(worker.sockets, SocketFactory)
        self.assertEqual(worker.params, [timeout, k, host, 23456, port, 0])


if __name__ == "__main__":
    unittest.main()
