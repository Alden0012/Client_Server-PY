import socket
import threading
class Server:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []
	def __init__(self):
		self.sock.bind(('0.0.0.0', 10000))
		self.sock.listen(1)
	def handler(self,c,a):
		while True:
			data = c.recv(1024)
			alias = str([a[0]]) + ":" + str(a[1])
			if not data:
				print(alias, "disconnected" )
				self.connections.remove(c)
				c.close()
				break;
			print(alias + ' says: ' + str(data,'utf-8'))
			self.broadcast_single(data);
	def run(self):
		while True:
				c, a = self.sock.accept()
				cThread = threading.Thread(target = self.handler, args = (c,a))
				cThread.daemon = True
				cThread.start()
				aThread = threading.Thread(target = self.broadcast)
				aThread.daemon = True
				aThread.start()
				self.connections.append(c)
				print(str([a[0]]) + ":" + str(a[1]), "connected" )
	def broadcast_single(self,data):
		for connection in self.connections:
				connection.send(data)
	def broadcast(self):
		while True:
			data = input("")
			if data != "Close":
				for connection in self.connections:
					connection.send(bytes(data, 'utf-8'))
					#print("Sending")
			else: 
				self.sock.close()

server_inst = Server()
server_inst.run()