# Web App (Don't know why I called it sensor_server_api)
# Created by Jessica Mong (Started: 07/31/2013) for Sensor_Project
# For my sanity, I will be referring to this as python script 2 (which happens to be my flask file)
# Python script 1 (pyserial.py) reads data from arduino and makes HTTP requests to add_event handler in python script 2

# (08/10) Abandoned flask megatutorial for now. I'm still using forms.py, config.py from the tutorial

from flask import Flask, flash, render_template, redirect, request
from flask import session, g, url_for 
from datetime import datetime
from twilio.rest import TwilioRestClient
from forms import LoginForm, RegistrationForm
import model

app = Flask (__name__)
app.config.from_object('config')

# app.secret_Key = "abcdefghjklkjf"


#(07/31)This app route renders a form that supplies fake data to the add_event
# Will be removed as soon as I can get HTTP requests working from pyserial 
#(08/05) Block of code was commented out. HTTP request now working.
#
# @app.route("/fake_data_form")
# def fake_data_form():
# 	return render_template("fake_data_form.html")

# Index is acting as both homepage and login
@app.before_request
def before_request():
	user_id = session.get("user_id")
	if user_id:
		user = model.session.query(model.User).get(user_id)
		g.user = user
	else:
		g.user = None

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
	form = LoginForm()
	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data

		user = model.session.query(model.User).filter(model.User.email==email).filter(model.User.password==password).first()

		if user:
			arduino = model.session.query(model.Arduino).filter(model.Arduino.user_id==user.id).first()
			events = model.session.query(model.Event).filter(model.Event.arduino_id==arduino.id).limit(10).all()
			session['user_id'] = user.id
			return render_template("hack_home.html", user=user, events=events)
			# return redirect("/home")
		else:
			flash('Sorry! This email and password combination does not exist')
			return render_template("hack_index.html", form=form)

	return render_template("hack_index.html", form=form)

# @app.route("/home", methods=['GET', 'POST'])
# def index():
# 	user = g.user
# 	arduino = model.session.query(model.Arduino).filter(model.Arduino.user_id==user.id).first()
# 	events = model.session.query(model.Event).filter(model.Event.arduino_id==arduino.id).limit(10).all()
# 	return render_template("hack_home.html", user=user, events=events)

@app.route("/register", methods=['GET', "POST"])
def register():
	form = RegistrationForm()
	return render_template("hack_register", form=form)


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