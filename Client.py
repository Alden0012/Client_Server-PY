import socket
class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	def __init__(self, address):
		self.sock.connect((address,10000))
		while True:
			self.sendMsg()
			#print("Sending")

	def sendMsg(self):
		self.sock.send(bytes(input(""), 'utf-8'))

client_inst = Client('104.45.152.207')