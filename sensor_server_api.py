# Web App (Don't know why I called it sensor_server_api)
# Created by Jessica Mong (Started: 07/31/2013) for Sensor_Project
# For my sanity, I will be referring to this as python script 2 (which happens to be my flask file)
# Python script 1 reads data from arduino and makes HTTP requests to add_event handler in python script 2

from flask import Flask, render_template, redirect, request
from flask import session, g, url_for 
from datetime import datetime
import model
from twilio.rest import TwilioRestClient

app = Flask (__name__)

app.secret_Key = "abcdefghjklkjf"

#(07/31)This app route renders a form that supplies fake data to the add_event
# Will be removed as soon as I can get HTTP requests working from pyserial 
@app.route("/fake_data_form")
def fake_data_form():
	return render_template("fake_data_form.html")

@app.route("/add_event", methods=["POST"])
def add_event():
	event = model.Event()

	event.arduino_id = request.form["id"]
	event.event = request.form["event"]
	event.timestamp = datetime.now()

	# event.timestamp = request.form["timestamp"] 
	# Sending datetime from pyserial isn't working, because it's being sent as a string
	# I have to find a way for it to send a datetime object

	model.session.add(event)
	model.session.commit()

	# print "Hey I'm here!!!", type(event.event) ##### Print to test if event.event is an integer

	#Code to send text message using Twilio API
	if event.event == 1:
		account_sid = "AC43217aee93d8775227e4a486a6e6e48f"
		auth_token = "352c071bc205bda5b8cfdc852c72f008"

		client = TwilioRestClient(account_sid, auth_token)

		sms = client.sms.messages.create(body = "Hey Jessica! There is power!!",
										to = "+19176916498",
										from_ = "+12167778433")
	return "I work!!!"

if __name__ == "__main__":
	app.run(debug = True)