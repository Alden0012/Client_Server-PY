#RUN ON BSP TERMINAL
import threading
import socket
import subprocess
import time
import os
class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	started = False
	roundOver = True
	ToSend = 0
	TheFlag = False
	ToBeSent = 0
	def __init__(self, address, port):
		self.sock.connect((address,port))
		self.runS1()
	def runS1(self): #connecting to server state
		data = self.sock.recv(1024)
		print(str(data,'utf-8'))
		#while !(str(data,'utf-8')):
		#	data = self.sock.recv(1024)
	    #	print(str(data,'utf-8'))
		self.runS2()
	def runS2(self): #game state
		print("Game Started!")
		self.started = True
		aThread = threading.Thread(target = self.recieveResponse)
		aThread.daemon = True
		aThread.start()
		while self.started:
			if(self.roundOver):
				time.sleep(4)
				self.sendMsg()
				self.roundOver = False
		aThread.join()
		self.ping_jtag()
		print("Thanks for playing!")
		os._exit(0)

	def wait(self):
		time.sleep(8)
		started = False
	def recieveResponse(self):
		while True:
			data = self.sock.recv(1024)
			print(str(data,'utf-8'))
			if(str(data,'utf-8')[0:9] == "Incorrect"):
				self.ToSend = int(str(data,'utf-8')[20]) 
				self.roundOver = True
			elif(str(data,'utf-8')[0:7] == "Correct"):
				self.ToSend = int(str(data,'utf-8')[18]) 
				self.roundOver = True
			elif(str(data,'utf-8')[0:6] == "Points"):
				self.ToSend = int(str(data,'utf-8')[8])
				self.roundOver = True
			if(str(data,'utf-8') == "e" or str(data,'utf-8') == ""):
				#print("Thanks for playing!")
				self.started = False
				break
		#os._exit(0)
	def recieveMsg(self):
		while True:

			data = self.sock.recv(1024)
			self.runS2()				
			
	def sendMsg(self):

		data = self.ping_jtag()

		self.sock.send(bytes(data, 'utf-8'))

	def ping_jtag(self):
		#pings the jtag with the letter t, when the fgpa recieves this through the jtag
		#it will respond with current accelerometer 
		if(self.ToSend > 9):
			self.ToBeSent = chr( ord('9') +  (self.ToSend - 9) )

		else:
			self.ToBeSent = self.ToSend
		self.ToBeSent = chr((ord(str(self.ToBeSent))-48)+98)
		inputCmd = "nios2-terminal.exe <<< " + str(self.ToBeSent)

		output = subprocess.run(inputCmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
		vals = output.stdout
		vals = vals.decode(encoding ='UTF-8',errors='ignore')
		vals = vals.split('<-->')
		return vals[1].strip()
    	
ServerAddr = input("Server Address: ")
ServerPort = int(input("Server Port: "))
client_inst = Client(ServerAddr,ServerPort)
