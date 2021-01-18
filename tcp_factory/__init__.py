from .worker import TCPWorker
from .sock_factory import SocketFactory
from .tcp_creator import TCPFactory


class TCPWorkerFactory:

	def __init__(self):
		self.sockets = SocketFactory()
		self.packets = TCPFactory()
		self.resulter = None

	def set_resulter(self, resulter):
		self.resulter = resulter

	def make(self, timeout, k, host, port, queue, seq):
		return TCPWorker(self.sockets,
						 self.packets,
						 self.resulter,
						 timeout, k, host, port, queue=queue, seq=seq)
