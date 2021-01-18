import socket


class SocketFactory:
	@staticmethod
	def make(timeout):
		s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
		s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
		s.settimeout(timeout)
		return s
