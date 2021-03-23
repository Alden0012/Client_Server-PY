import socket
import threading
import time
import random
class Server:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []
	QuestionBank = {"Choose A": "A", "Choose B": "B" ,"Choose C": "C" ,"Choose D": "D"}
	Players = {}
	Recieved = {}
	AliasToC = {}
	maxPlayers = 3
	def __init__(self):
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('0.0.0.0', 10000))
		self.sock.listen(1)
	def handler(self,c,a):
		while True:
			data = c.recv(1024)
			alias = a
			if not data:
				print(alias, "disconnected" )
				self.connections.remove(c)
				c.close()
				break
			self.Recieved[alias] = str(data,'utf-8')
			#print(alias + ' says: ' + str(data,'utf-8'))
			print(self.Recieved)
			#self.broadcast_single(data)
	def runS1(self):
		#State 1: Connecting to other devices
		while True:
				c, a = self.sock.accept()
				#cThread = threading.Thread(target = self.handler, args = (c,a))
				#cThread.daemon = True
				#cThread.start()
				#aThread = threading.Thread(target = self.broadcast)
				#aThread.daemon = True
				#aThread.start()
				self.connections.append(c)
				alias =  str(a[1])
				self.Players[alias] = 0
				self.Recieved[alias] = 0
				self.AliasToC[alias] = c
				print(str(a[1]), "connected" )
				
				if len(self.connections) > self.maxPlayers-1:
					break
		print("All players connected! Beginning Game")
		time.sleep(3)
		for connection in self.connections:
					connection.send(bytes('c', 'utf-8'))
		self.runS2();				
	def runS2(self):
		for key in self.AliasToC.keys():
			self.AliasToC[key].send(bytes("Get Ready! Player: " + str(key) + "\n", 'utf-8'))
		i = 1
		while i < 11: 
			#for connection in self.connections:
			#	connection.send(bytes("Round " + str(i), 'utf-8'))
			Question, answer = random.choice(list(self.QuestionBank.items())) 
			for connection in self.connections:
				connection.send(bytes(Question, 'utf-8'))
			for key in self.AliasToC.keys():
				cThread = threading.Thread(target = self.handler, args = (self.AliasToC[key],key))
				cThread.daemon = True
				cThread.start()
			time.sleep(10)
			print("Round Over!")
			print(self.Recieved)
			for connection in self.connections:
				connection.send(bytes("Round " + str(i) + " over!"+ "\n", 'utf-8'))
			for key in self.Recieved.keys():
				if answer == self.Recieved[key]:
					self.Players[key] += 1
					self.AliasToC[key].send(bytes("Correct!\n" + "\n", 'utf-8'))
					self.AliasToC[key].send(bytes("Points: " + str(self.Players[key]) + "\n", 'utf-8'))
				else:
					self.AliasToC[key].send(bytes("Incorrect!\n\n", 'utf-8'))
					self.AliasToC[key].send(bytes("Points: " + str(self.Players[key]) + "\n", 'utf-8'))
			print(self.Players)
			i = i + 1
		for connection in self.connections:
				connection.send(bytes("Game over!"+ "\n", 'utf-8'))
				connection.send(bytes(str(self.Players)+ "\n", 'utf-8'))
				connection.send(bytes(str("e")+ "\n", 'utf-8'))


	def broadcast_single(self,data):
		for connection in self.connections:
				connection.send(data)
	def broadcast(self):
		while True:
			data = input("")
			if data != "Close":
				for connection in self.connections:
					connection.send(bytes(data, 'utf-8'))
			if data == "Close": 
				self.sock.shutdown(socket.SHUT_RDWR)
				exit()

server_inst = Server()
server_inst.runS1()
