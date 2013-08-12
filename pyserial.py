#This script does not import my webapp so it's not dependent on it (kinda)

import serial
import requests
from datetime import datetime
#########################################################
# Arduino Config Information 
global arduino_id       #Still need to figure out how I will use this part
global arduino_key      #for arduino authentication purposes
#########################################################


def open_serial_port():
	ser = serial.Serial('/dev/ttyACM0', 9600)
	# ser.port =  #This changes to ACM1 sometimes
	# ser.baudrate = 9600
	# ser.open()
	return ser

def read_from_serial(ser):
	# print "Hi!!!"               ALL PRINT STATEMENTS ARE FOR DEBUGGING
	# print ser.inWaiting()
	while (ser.inWaiting() == 0 or ser.inWaiting() > 0):
		# print "I'm here"
		print "Please push button"
		event = ser.readline().rstrip()
		# print event
		# print (event=="1")
	#Dictionary that contains information from arduino
		params = {"id" : 1, 
				"event" : int(event)}
				# "timestamp" : datetime.now()}
		req = requests.post("http://localhost:5000/add_event", data = params)
		print req

def main():
	ser = open_serial_port()
	ser.flushInput()
	while 1:
		read_from_serial(ser)

if __name__ == "__main__":
	main()