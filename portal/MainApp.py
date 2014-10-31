import datetime
import ConfigParser
import csv
import os
import re
import sys
import glob
import pprint
from sqlalchemy.sql import func
from flask import Flask
from flask import render_template
from flask import request
from flask import session
import FileOperators
import AdditionalTools
config = ConfigParser.ConfigParser()
rconfig = ConfigParser.RawConfigParser()
global_inspath = '/home/jin/projects/worklog/'
from flask.ext.sqlalchemy import SQLAlchemy
from models import db, User, Customer, Admin, WorkLog, Reports, Currencies, Settings

class WorkLogger():
	def __init__(self):
		self.clients = Customer.query.all() 
	def list_clients(self):
		return render_template('testy.htm', clist=self.clients)

class Parsers():
	def db_txt_parser(self,_text):
		parsed_text = []
		for text_tuple in _text:
			for item in text_tuple:
				parsed_item = item.decode('raw_unicode_escape')
				parsed_text.append(str(parsed_item))
		return parsed_text
		
	def db_long_parser(self,_number):
		parsed_numbers = []
		if len(_number) > 1:
			for a in range(len(_number)):
				pre_number = _number[a]
				for item in pre_number:
					parsed_number = item
					parsed_numbers.append(int(parsed_number))
			return parsed_numbers
		else:
			pre_number = _number[0]
			for item in pre_number:
				parsed_number = item
			return parsed_number
			
	def personal_data_parser(self,_uid):
		p = Parsers()
		client_fname = WorkLog.query.with_entities(Customer.firstname).filter_by(uid=_uid).all()
		first_name = str(p.db_txt_parser(client_fname)).strip("[]'")
		client_lname = WorkLog.query.with_entities(Customer.lastname).filter_by(uid=_uid).all()
		last_name = str(p.db_txt_parser(client_lname)).strip("[]'")
		client_email = WorkLog.query.with_entities(Customer.email).filter_by(uid=_uid).all()
		email = str(p.db_txt_parser(client_email))
		client_company = WorkLog.query.with_entities(Customer.clientid).filter_by(uid=_uid).all()
		company = str(p.db_txt_parser(client_company)).strip("[]'")
		return [str(first_name + ' ' + last_name), str(email), str(company)]
				
				
				
class ClientsManage():
	def __init__(self):
		self.clients = Customer.query.with_entities(Customer.clientid)
	def list_clients(self):
		p = Parsers()
		customer_list = p.db_txt_parser(self.clients)
		return render_template('selector.htm', customer_list=customer_list)

class BackendMainPage():
	def __init__(self):
		if 'clientid' in session:
			self.clientid = session['clientid']
		else:
			self.clientid = request.form['client_sel']
			session['clientid'] = self.clientid
		p = Parsers()
		self.client_data = []
		self.raw_uid = Customer.query.with_entities(Customer.uid).filter_by(clientid=self.clientid).all()
		self.uid = p.db_long_parser(self.raw_uid)
	
	def work_items_creator(self,_uid):
		workitems = WorkLog.query.with_entities(WorkLog.date_start, WorkLog.date_stop, WorkLog.duration_hours, 
		WorkLog.cost, WorkLog.note).order_by(WorkLog.date_start.desc()).filter_by(uid=_uid).all()
		return (workitems)
	
	def work_durations(self,_uid):
		p = Parsers()
		a = AdditionalTools.AdditionalTools()
		# Total duration
		work_durations = p.db_long_parser(WorkLog.query.with_entities(WorkLog.duration).filter_by(uid=_uid).all())
		total_duration = 0
		if isinstance(work_durations, list):
			for item in work_durations:
				total_duration = total_duration + item
			total_duration_human = a.time_human(total_duration)
		else:
			total_duration_human = a.time_human(work_durations)
		# Current month duration
		month_now = datetime.datetime.now().strftime("%Y-%m")
		month_first_day = month_now + "-01 00:00:00"
		month_durations = p.db_long_parser(WorkLog.query.filter(WorkLog.date_start > month_first_day).with_entities(WorkLog.duration).filter_by(uid=_uid).all())
		if isinstance(month_durations, list):
			total_month_duration = 0
			for item in month_durations:
				total_month_duration = total_month_duration + item
				total_month_duration_human = a.time_human(total_month_duration)
		else:
			total_month_duration_human = a.time_human(month_durations)
		return [total_duration_human,total_month_duration_human]
	
	def work_monies(self,_uid):
		p = Parsers()
		# Customer rate and currency
		base_rate = Customer.query.with_entities(Customer.rate).filter_by(uid=_uid).all()
		rate = p.db_long_parser(base_rate)
		currencyid = p.db_long_parser(Customer.query.with_entities(Customer.currency).filter_by(uid=_uid).all())
		base_currency = p.db_txt_parser(Currencies.query.with_entities(Currencies.currency).filter_by(id=currencyid).all())
		# Total monies
		work_costs = p.db_long_parser(WorkLog.query.with_entities(WorkLog.cost).filter_by(uid=_uid).all())
		total_work_cost = 0
		if isinstance(work_costs, list):
			for item in work_costs:
				total_work_cost = total_work_cost + item
		else:
			total_work_cost = work_costs
		# This month monies
		month_now = datetime.datetime.now().strftime("%Y-%m")
		month_first_day = month_now + "-01 00:00:00"
		month_costs = p.db_long_parser(WorkLog.query.filter(WorkLog.date_start > month_first_day).with_entities(WorkLog.cost).filter_by(uid=_uid).all())
		if isinstance(month_costs, list):
			total_month_cost = 0
			for item in month_costs:
				total_month_cost = total_month_cost + item
		else:
			total_month_cost = month_costs
		return [rate, base_currency, total_work_cost, total_month_cost]
		
	def main_page(self):
		uid = self.uid
		b = BackendMainPage()
		p = Parsers()
		# Information variables
		client = p.personal_data_parser(uid)
		workitems = b.work_items_creator(uid)
		total_duration = b.work_durations(uid)[0]
		length = len(b.work_durations(uid))
		total_month_duration = b.work_durations(uid)[1]
		rate = b.work_monies(uid)[0]
		currency = str(b.work_monies(uid)[1]).strip("[]'")
		monies = b.work_monies(uid)[2]
		month_monies = b.work_monies(uid)[3]
		# CSS variables
		tbutton='start'
		tbutton_class='btn-primary'
		note_class = 'hidden'
		status_class = 'hidden'
		# Render
		return render_template('logger.htm',
		rate=rate,
		currency=currency,
		total_duration=total_duration, 
		total_month_duration=total_month_duration,
		workitems=workitems,
		client_name=client[0], 
		monies=monies, 
		month_monies=month_monies, 
		company_name=client[2], 
		uid=uid,
		tbutton=tbutton,
		tbutton_class=tbutton_class,
		note_class=note_class,
		status_class=status_class)

class WorkCounter():
	def __init__(self):
		p = Parsers()
		b = BackendMainPage()
		# Session
		if 'clientid' in session:
			self.clientid = session['clientid']
		if 'currency' in session:
			self.curr = session['currency']
		if 'rate' in session:
			self.rate = session['rate']
		if 'total_time' in session:
			self.total_time = session['total_time']
		if 'start' in session:
			self.start = session['start']
		if 'startt' in session:
			self.startt = session['startt']
		if 'inifile' in session:
			self.inifile = session['inifile']
		if 'csvfile' in session:
			self.csvfile = session['csvfile']	
		if 'total_time_human' in session:
			self.total_time_human = session['total_time_human']
		if 'total_time_hours' in session:
			self.total_time_hours = session['total_time_hours']
		if 'monies' in session:
			self.monies = session['monies']	
		if 'month_monies' in session:
			self.month_monies = session['month_monies']	
		if 'month_work_human' in session:
			self.month_work_human = session['month_work_human']	
		self.client_data = []
		self.raw_uid = Customer.query.with_entities(Customer.uid).filter_by(clientid=self.clientid).all()
		self.uid = p.db_long_parser(self.raw_uid)
		# Information variables
		uid = self.uid
		self.client = p.personal_data_parser(uid)
		self.workitems = b.work_items_creator(uid)
		self.total_duration = b.work_durations(uid)[0]
		self.length = len(b.work_durations(uid))
		self.total_month_duration = b.work_durations(uid)[1]
		self.rate = b.work_monies(uid)[0]
		self.currency = str(b.work_monies(uid)[1]).strip("[]'")
		self.monies = b.work_monies(uid)[2]
		self.month_monies = b.work_monies(uid)[3]

			
	def start_counting(self):
		error = None
		b = BackendMainPage()
		p = Parsers()
		uid = self.uid
		# note the start time of the work
		start = datetime.datetime.now()
		startt = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		# put some variables for page render
		finisht = 'ongoing'
		tbutton='stop'
		tbutton_class='btn-warning'
		note_class='form-control'
		status_class=''
		# send data to session
		session['start'] = start
		session['startt'] = startt
		return render_template('logger.htm',
		rate=self.rate,
		currency=self.currency,
		total_duration=self.total_duration, 
		total_month_duration=self.total_month_duration,
		workitems=self.workitems,
		client_name=self.client[0], 
		monies=self.monies, 
		month_monies=self.month_monies, 
		company_name=self.client[2], 
		uid=uid,tbutton=tbutton,
		tbutton_class=tbutton_class,
		note_class=note_class,
		status_class=status_class,
		start_time=startt,
		stop_time=finisht)
	
	def stop_counting(self):
		a = AdditionalTools.AdditionalTools()
		uid = self.uid
		total_time = self.total_duration
		# note the work finish time
		finish = datetime.datetime.now()
		finisht=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		# count the worktime
		delta = finish - self.start
		work_time=str(datetime.timedelta(seconds=delta.seconds))
		# get work note from input
		note = request.form['worknote']
		# put total time in a human way
		time_hours = a.time_hours(delta.seconds)
		time_precise = a.time_human(delta.seconds)
		# count monies
		session_monies = self.rate*time_hours
		# save worklog entry in worklog
		new_record = WorkLog(uid,self.startt,finisht,delta.seconds,time_precise,int(session_monies),note)
		db.session.add(new_record)
		db.session.commit()
		# put some variables for page rendering
		tbutton='start'
		tbutton_class='btn-primary'
		note_class='hidden'
		status_class=''
		# render page
		return render_template('logger.htm',
		rate=self.rate,
		currency=self.currency,
		total_duration=self.total_duration, 
		total_month_duration=self.total_month_duration,
		workitems=self.workitems,
		client_name=self.client[0], 
		monies=self.monies, 
		month_monies=self.month_monies, 
		company_name=self.client[2], 
		uid=self.uid,
		tbutton=tbutton,
		tbutton_class=tbutton_class,
		note_class=note_class,
		status_class=status_class,
		start_time=self.start,
		stop_time=finisht)

	
class MainApp():
	def __init__(self):
		# installation path
		self.inspath = global_inspath
		# global conf
		self.global_config = "/etc/worklog_global.ini"
		# pass keys from session if they exist
		if 'clientid' in session:
			self.clientid = session['clientid']
		if 'currency' in session:
			self.curr = session['currency']
		if 'rate' in session:
			self.rate = session['rate']
		if 'total_time' in session:
			self.total_time = session['total_time']
		if 'start' in session:
			self.start = session['start']
		if 'startt' in session:
			self.startt = session['startt']
		if 'inifile' in session:
			self.inifile = session['inifile']
		if 'csvfile' in session:
			self.csvfile = session['csvfile']	
		if 'total_time_human' in session:
			self.total_time_human = session['total_time_human']
		if 'total_time_hours' in session:
			self.total_time_hours = session['total_time_hours']
		if 'monies' in session:
			self.monies = session['monies']	
		if 'month_monies' in session:
			self.month_monies = session['month_monies']	
		if 'month_work_human' in session:
			self.month_work_human = session['month_work_human']	
	
	# firstpage
	def add_worktime(self):
		f = FileOperators.FileOperators()
		clientslisting = f.clisting()
		session.pop('clientid', None)
		return render_template('step1.htm', clientlist=clientslisting,savestatus="",savestatusclass="hidden")
