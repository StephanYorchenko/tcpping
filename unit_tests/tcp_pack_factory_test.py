import unittest

from tcp_factory import TCPFactory


class TCPPackFactoryTest(unittest.TestCase):
	data = {
			('127.0.0.1', '127.0.0.1', 8479, 5432, 0,
			 59017): b'E\x00\x00(!\x1f\x00\x00\xff\x06\x00\n\x7f\x00\x00'
					 b'\x01\x7f\x00\x00\x01\xe6\x89\x158\x00\x00\x00\x00'
					 b'\x00\x00\x00\x01P\x02\x00\x00\xb6\x1d\x00\x00',
			('192.168.43.100', '8.8.8.8', 8479, 5432, 0,
			 59017): b'E\x00\x00(!\x1f\x00\x00\xff\x06\x00\n\xc0\xa8+d'
					 b'\x08\x08\x08\x08\xe6\x89\x158\x00\x00\x00\x00'
					 b'\x00\x00\x00\x01P\x02\x00\x00\xb8\x03\x00\x00'
	}

	def setUp(self) -> None:
		self.factory = TCPFactory()

	def test_checksum(self):
		m = [
				(
						b'\xc0\xa8+d\n`\x12\xc8\x00\x06\x00\x14\xaf;09'
						b'\x00\x00\x00\x00\x00\x00\x00\x01P\x02\x00\x00'
						b'\x00\x00\x00\x00',
						51000),
				(
						b'\xc0\xa8+d\n`\x12\xc8\x00\x06\x00\x14\xa0\r09'
						b'\x00\x00\x00\x00\x00\x00\x00\x01P\x02\x00\x00'
						b'\x00\x00\x00\x00',
						54886),
		]
		for i in m:
			self.assertEqual(self.factory.checksum(i[0]), i[1])

	def test_generate(self):
		for k, v in self.data.items():
			self.assertEqual(self.factory.generate(*k), v)


if __name__ == '__main__':
	unittest.main()
