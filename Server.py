import socket
import threading
import time
import random
import codecs
import operator
class Server:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connections = []
	QuestionBank = {}
	QuestionTime = {}
	NameList = {"Sage Buzzard","Aromatic Raven","Fat Parrot","Sweet Bonobo", "Ambitious Muskox", "Fiery Axolotl", "Roaring Adder", "Careful Deer", "Lovely Alpaca", "Cerise Hare", "Terrestrial Longhorn", "Beige Chicken", "Jolly Platypus", "Adept Trout"}
	PlayerNames = {}
	Players = {}
	Leaderboard = {}
	Recieved = {}
	AliasToC = {}
	InputFile = "Questions.txt"
	maxPlayers = 3
	Rounds = 5
	def __init__(self,players,rounds):
		self.maxPlayers = int(players)
		self.Rounds = int(rounds)
		print("Waiting for players")
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
		#preamble: loading questions in
		f = open(self.InputFile)
		for line in f:
			(key, val, qtime) = line.strip().split("^",2)
			self.QuestionBank[key.replace('\\n','\n')] = val.strip()
			self.QuestionTime[key.replace('\\n','\n')] = qtime.strip()
		#for key in self.QuestionBank.keys():

			#print(key,self.QuestionBank[key])
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
				choice = random.choice(list(self.NameList))
				self.PlayerNames[alias] = choice
				self.NameList.remove(choice)
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
			self.AliasToC[key].send(bytes("Get Ready! Player: " + str(self.PlayerNames[key]) + "\n\n", 'utf-8'))
		i = 1
		while i < (self.Rounds+1): 
			#for connection in self.connections:
			#	connection.send(bytes("Round " + str(i), 'utf-8'))
			Question, answer = random.choice(list(self.QuestionBank.items())) 
			self.QuestionBank.pop(Question)
			for connection in self.connections:
				connection.send(bytes(Question, 'utf-8'))
			for key in self.AliasToC.keys():
				cThread = threading.Thread(target = self.handler, args = (self.AliasToC[key],key))
				cThread.daemon = True
				cThread.start()
			time.sleep(int(self.QuestionTime[Question]))
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
		FinishingData = "\n----------------\nLeaderboard\n----------------\n\n"
		self.Leaderboard = {k: v for k, v in sorted(self.Players.items(), key=lambda item: item[1])}
		for key in sorted(self.Players, key = self.Players.get,reverse = True):
			FinishingData = FinishingData + str(self.PlayerNames[key]) + " : " + str(self.Players[key]) + "\n"
		for key in self.Recieved.keys():
			self.AliasToC[key].send(bytes("Points: " +str(self.Players[key]) +"\n", 'utf-8'))
		for connection in self.connections:

				connection.send(bytes("Game over!"+ "\n", 'utf-8'))
				connection.send(bytes(str(FinishingData)+ "\n", 'utf-8'))
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
playerCount = input("Number of players?: ")
roundinput = input("Number of rounds?: ")
server_inst = Server(playerCount,roundinput)
server_inst.runS1()
