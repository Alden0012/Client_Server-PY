#RUN ON BSP TERMINAL

import socket
import subprocess
class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	def __init__(self, address):
		self.sock.connect((address,10000))
	def run(self):	
		while True:
			self.sendMsg()
			#print("Sending")
	def sendMsg(self):
		self.sock.send(bytes(input(""), 'utf-8'))
		self.run()

	def ping_jtag(self):
		#pings the jtag with the letter t, when the fgpa recieves this through the jtag
		#it will respond with current accelerometer 
		inputCmd = "nios2-terminal <<< t"
		output = subprocess.run(inputCmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
		vals = output.stdout
		return vals;
    	

client_inst = Client('104.45.152.207')