import unittest

from tcp_factory import SocketFactory


class SockFactoryTest(unittest.TestCase):
	def setUp(self) -> None:
		self.sock_factory = SocketFactory()

	def test_assert_permission_error(self):
		for i in range(10):
			self.assertRaises(OSError, self.sock_factory.make, i)

# def test_socket(self):
# 	with self.sock_factory.make(2) as sock:
# 		self.assertIsInstance(sock, socket.socket)
# Raises Permission Error


if __name__ == '__main__':
	unittest.main()
