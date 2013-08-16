from flask.ext.wtf import Form, TextField, PasswordField, BooleanField, FormField, IntegerField, StringField
from flask.ext.wtf import Required

CSRF_ENABLED = True
SECRET_KEY = "jkasdhdfhbjhfbid"

class LoginForm(Form):
	email = TextField('email', validators=[Required()])
	password = PasswordField('password', validators=[Required()])
	remember_me = BooleanField('remember_me', default = False)

# class TelephoneForm(Form):
#     country_code = IntegerField('country_code', validators =[Required()])
#     area_code    = IntegerField('area_code', validators =[Required()])
#     number       = StringField('number')

class RegistrationForm(Form):
	first_name = TextField('first_name', validators=[Required()])
	last_name = TextField('last_name', validators=[Required()])
	phone = TextField('phone', validators=[Required()])
	city = TextField('city', validators=[Required()])
	state = TextField('state', validators=[Required()])
	# address = TextField('address', validators=[Required()])
	email = TextField('email', validators=[Required()])
	password = PasswordField('password', validators=[Required()])
	# I would like to do another password field here to make sure that the user inputs the right password
	arduino_key = TextField('arduino_key', validators=[Required()])