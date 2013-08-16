# This script will be on the users side, theoretically.
#This script does not import my webapp so it's not dependent on it (kinda)

import serial
import requests
from datetime import datetime
#########################################################
# Arduino Config Information 
# Still need to figure out how I will use this part
# (08/14) Ok! Figured it out! This script will be on the users side ideally, so it's ok if it can contain specific information about the arduino
global ARDUINO_KEY   #for arduino authentication purposes
ARDUINO_KEY = "ABCDEFGHIJ"
#########################################################


def open_serial_port():
	ser = serial.Serial('/dev/ttyACM0', 9600)
	# ser.port =  #This changes to ACM1 sometimes
	# ser.baudrate = 9600
	# ser.open()
	return ser

def read_from_serial(ser):
	global ARDUINO_KEY
	# print "Hi!!!"               ALL PRINT STATEMENTS ARE FOR DEBUGGING
	# print ser.inWaiting()

	# I used the while loop when I was using a button to simulate the sensor. Now, sensor is working!
	# while (ser.inWaiting() == 0 or ser.inWaiting() > 0):
	# 	# print "I'm here"
	# 	print "Please push button"
	state = 0
	req = "abc"
	event = ser.readline().rstrip()
	print event

	if event == "On":
		state = 1
		params = {"key" : ARDUINO_KEY, 
				"event" : state}
		req = requests.post("http://localhost:5000/add_event", data = params)
		print "event on"
		print req
	elif event == "Off":
		state = 0 
		params = {"key" : ARDUINO_KEY, 
				"event" : state}
		req = requests.post("http://localhost:5000/add_event", data = params)
		print "event off"
		print req
	elif event:
		params = {"key": ARDUINO_KEY,
				"reading" : int(event)}
		req = requests.post("http://localhost:5000/add_power_reading", data = params)
		print "reading:"
		print req


	# print event
	# print (event=="1")
	#Dictionary that contains information from arduino for post request
	
			# "timestamp" : datetime.now()} // Setting the datetime from here will send a string 
											#  to the database instead of a datetime object
	

# def populate_csv(filename, arduino_id, apparent_power, timestamp)

def main():
	ser = open_serial_port()
	ser.flushInput()
	while 1:
		read_from_serial(ser)

if __name__ == "__main__":
	main()