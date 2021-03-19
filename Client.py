#RUN ON BSP TERMINAL
import threading
import socket
import subprocess
import time
import os
class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	started = False
	def __init__(self, address):
		self.sock.connect((address,10000))
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
		started = True
		aThread = threading.Thread(target = self.recieveResponse)
		aThread.daemon = True
		aThread.start()
		while started:
			time.sleep(1.3)
			self.sendMsg()
		aThread.stop()
		print("Thanks for playing!")
		data = self.sock.recv(1024)
		print(str(data,'utf-8'))
	def wait(self):
		time.sleep(8)
		started = False
	def recieveResponse(self):
		while True:
			data = self.sock.recv(1024)
			print(str(data,'utf-8'))
			if(str(data,'utf-8') == "e" or str(data,'utf-8') == ""):
				started = False
				break
		print("Thanks for playing!")
		os._exit(0)
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
		inputCmd = "nios2-terminal.exe <<< t"
		output = subprocess.run(inputCmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
		vals = output.stdout
		vals = vals.decode(encoding ='UTF-8',errors='ignore')
		vals = vals.split('<-->')
		return vals[1].strip()
    	

client_inst = Client('104.45.152.207')