import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Float

engine = create_engine("sqlite:///sensor_proj.db", echo = True)
session = scoped_session(sessionmaker(bind = engine,
									autocommit = False,
									autoflush = False))

Base = declarative_base()
Base.query = session.query_property()


##### Class declarations here
class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	phone = Column(String(11))
	first_name = Column(String(32))
	last_name = Column(String(32))
	# address = Column(String(128)) I need to avoid stalkers so I can't ask for exact address
	# instead: I'll just ask for city and state
	city = Column(String(32))
	state = Column(String(32))
	#country is automatically Nigeria
	email = Column(String(32), nullable = True)
	password = Column (String(32))

class Arduino(Base):
	__tablename__ = "arduinos"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey('users.id'))
	key = Column(String(10))

	owner = relationship("User", backref = backref("arduino", order_by = id))

class Event(Base):
	__tablename__ = "events"

	id = Column(Integer, primary_key = True)
	arduino_key = Column(Integer, ForeignKey('arduinos.key'))
	event = Column(Integer) #Using 0 or 1. Might want to change to bool
	timestamp = Column(DateTime)

	arduino = relationship("Arduino", backref = backref("events", order_by = id))

class Power(Base):
	__tablename__ = "power"

	id = Column(Integer, primary_key = True)
	arduino_key = Column(Integer, ForeignKey('arduinos.key'))
	reading = Column(Float)
	timestamp = Column(DateTime)

	arduino = relationship("Arduino", backref = backref("power", order_by = id))
##### Class declarations end

def main():
	pass

if __name__ == "__main__":
	main()