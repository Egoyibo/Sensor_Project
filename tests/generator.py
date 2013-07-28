import test_model
from random import randint
from datetime import datetime

import twilio
from twilio.rest import TwilioRestClient

#################################################
account_sid = "<input>"
auth_token = "<input>"
#################################################
client = TwilioRestClient(account_sid, auth_token)
#################################################

def create_new_event():
	arduino_id = 1;
	event_no = randint(0,4)

	event = test_model.Event()
	event.arduino_id = arduino_id
	event.event = event_no
	event.timestamp = datetime.now()

	test_model.session.add(event)
	test_model.session.commit()

	if event_no == 1:
		sms = client.sms.messages.create(body = "Hey Jessica! Power has been restored!",
										to = event.arduino.owner.phone,
										from_ = "+12167778433")



def main():
	create_new_event()

if __name__ == "__main__":
	main()