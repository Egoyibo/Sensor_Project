# Web App (Don't know why I called it sensor_server_api)
# Created by Jessica Mong (Started: 07/31/2013) for Sensor_Project
# For my sanity, I will be referring to this as python script 2 (which happens to be my flask file)
# Python script 1 (pyserial.py) reads data from arduino and makes HTTP requests to add_event handler in python script 2

# (08/10) Abandoned flask megatutorial for now. I'm still using forms.py, config.py from the tutorial

from sqlalchemy import desc
from flask import Flask, flash, render_template, redirect, request
from flask import session, g, url_for 
from datetime import datetime
from twilio.rest import TwilioRestClient
from forms import LoginForm, RegistrationForm
import json
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
			events = events = model.session.query(model.Event).order_by(desc(model.Event.id)).filter(model.Event.arduino_key==arduino.key).limit(10).all()
			session['user_id'] = user.id

			#Now on to the graph data
			user_arduino_key = model.session.query(model.Arduino).filter(model.Arduino.user_id==user.id).first().key
			all_graph_readings = model.session.query(model.Power).filter(model.Arduino.key==user_arduino_key).all() #for now

			graph_readings = []
			for graph_reading in all_graph_readings:
				graph_reading_secs = (graph_reading.timestamp - datetime(1970,1,1)).total_seconds()

				each_reading_info = {"x": graph_reading_secs, "y": graph_reading.reading}
				graph_readings.append(each_reading_info)


			json_graph_readings = json.dumps(graph_readings)
			return render_template("hack_home_test.html", user=user, events=events, data=json_graph_readings)
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
	if form.validate_on_submit():
		# Need to check if user and arduino are already in database to avoid duplicates

		check_user = model.session.query(model.User).filter(model.User.email==form.email.data).first()
		check_user_phone = model.session.query(model.User).filter(model.User.phone==form.phone.data).first()
		check_arduino = model.session.query(model.Arduino).filter(model.Arduino.key==form.arduino_key.data).first()

		if check_user or check_user_phone or check_arduino:
			flash("This account already exists")
			return redirect("/register")
		else:
			user = model.User()

			user.phone = form.phone.data
			user.first_name = form.first_name.data
			user.last_name = form.last_name.data
			user.city = form.city.data
			user.state = form.state.data
			user.email = form.email.data
			user.password = form.password.data

			model.session.add(user)
			model.session.commit()
			#I committed the user first so that I can have a user_id for the arduino

			arduino = model.Arduino()

			arduino.user_id = user.id
			arduino.key = form.arduino_key.data

			model.session.add(arduino)
			model.session.commit()

			session["user_id"] = user.id
			# raise Exception("Nopr")
			events = model.session.query(model.Event).filter(model.Event.arduino_key==arduino.key).order_by(desc(model.Event.id)).limit(10)
			#for testing
			# for event in events:
			# 	print "I'm HERE!!!!!!!!!", event.id

			return render_template("hack_home.html", user=user, events=events)

	return render_template("hack_register.html", form=form)

@app.route("/logout")
def logout():
	session["user_id"] = None
	flash("Successfully logged out!")
	return redirect("/")

@app.route("/add_event", methods=["POST"])
def add_event():
	#Validate arduino
	client_arduino_key = model.session.query(model.Arduino).filter(model.Arduino.key==request.form["key"]).first().key
	if client_arduino_key:

		event = model.Event()

		event.arduino_key = client_arduino_key
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
		return "I work!!! <EVENT>"
	else:
		raise Exception("ARDUINO IS NOT RECOGNIZED")

@app.route("/add_power_reading", methods=["POST"])
def add_power_reading():
	power = model.Power()

	power.arduino_key = request.form["key"]
	power.reading = request.form["reading"]
	power.timestamp = datetime.now()

	model.session.add(power)
	model.session.commit()

	return "I work also!!! <POWER>"

@app.route("/display_power_reading")
def display_power_reading():
	# readings = model.session.query(model.Power)
	# return render_template("test_rickshaw.html")
	return render_template("hack_power_graph.html")

if __name__ == "__main__":
	app.run(debug = True)