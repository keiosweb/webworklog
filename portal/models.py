from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import MainApp

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key = True)
	clientid = db.Column(db.String(100))
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(54))
   
	def __init__(self, clientid, firstname, lastname, email, password):
		self.clientid = clientid.lower()
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)
     
	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)
   
	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

class Admin(db.Model):
	__tablename__ = 'admins'
	uid = db.Column(db.Integer, primary_key = True)
	userid = db.Column(db.String(100))
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique=True)
	pwdhash = db.Column(db.String(54))

	def __init__(self, userid, firstname, lastname, email, password):
		self.userid = userid.lower()
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(password)
     
	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)
   
	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

class Customer(db.Model):
	__tablename__ = 'customers'
	uid = db.Column(db.Integer, primary_key = True)
	clientid = db.Column(db.String(100))
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	rate = db.Column(db.Integer)
	currency = db.Column(db.Integer)
	email = db.Column(db.String(120), unique=True)
	def __init__(self, clientid, firstname, lastname, email):
		self.clientid = clientid.lower()
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.rate = rate
		self.currency = currency
		self.email = email.lower()
	def __repr__(self):
		return ('%r, %r, %r, %r', '%r') % (str(self.clientid), str(self.firstname), 
		str(self.lastname), str(self.email), int(rate), int(currency))
        
class WorkLog(db.Model):
	__tablename__ = 'worklogs'
	id = db.Column(db.Integer, primary_key = True)
	uid = db.Column(db.Integer)
	date_start = db.Column(db.Date) 
	date_stop = db.Column(db.Date) 
	duration = db.Column(db.Integer)
	duration_hours = db.Column(db.Time)
	cost = db.Column(db.Integer)
	note = db.Column(db.String(200))
	
	def __init__(self, uid, date_start, date_stop, duration, duration_hours, cost, note):
		self.uid = uid
		self.date_start = date_start 
		self.date_stop = date_stop
		self.duration = duration
		self.duration_hours = duration_hours
		self.cost = cost
		self.note = note
	def __repr__(self):
		return ('%r, %r, %r, %r, %r, %r, %r') % (int(self.uid), self.date_start, self.date_stop, int(self.duration), self.duration_hours, int(self.cost), str(self.note))
				
class Reports(db.Model):
	__tablename__ = 'reports'
	id = db.Column(db.Integer, primary_key = True)
	month = db.Column(db.String(100))
	total_time = db.Column(db.String(100))
	total_earnings = db.Column(db.String(100))
	def __init__(self, clientid, rate, currencyid):
		self.month = month
		self.total_time = total_time
		self.total_earnings = total_earnings
		
class Currencies(db.Model):
	__tablename__ = 'currencies'
	id = db.Column(db.Integer, primary_key = True)
	currency = db.Column(db.String(100))
	
	def __init__(self, currency):
		self.currency = currency
		
class Settings(db.Model):
	__tablename__ = 'settings'
	id = db.Column(db.Integer, primary_key = True)
	clientid = db.Column(db.String(100))
	rate = db.Column(db.Integer)
	currencyid = db.Column(db.Integer)
	def __init__(self, clientid, rate, currencyid):
		self.clientid = clientid
		self.rate = rate
		self.currencyid = currencyid
