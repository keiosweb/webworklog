import time
import datetime
import ConfigParser
import csv
import os
import re
import argparse
import sys
import glob
from mako.template import Template
from flask import Flask
from flask import render_template
from flask import request
from flask import session

# some initial things for whole app
app = Flask(__name__)
config = ConfigParser.ConfigParser()
rconfig = ConfigParser.RawConfigParser()

# global special functions
def specialmatch(strg, search=re.compile(r'[^a-z0-9]').search):
			return not bool(search(strg))
def remove_extension(s):
		return s[0:-4]

# depreciated
class CounterManage():
	def __init__(self):
		self.inspath = '/home/jin/projects/worklog/'
	
	def clisting(self):
		c = CounterManage()
		csvfiles = glob.glob('%s/db/*.csv' % self.inspath)
		csvlisting = [os.path.basename(x) for x in csvfiles]
		clientslisting = [remove_extension(s) for s in csvlisting]
		return clientslisting

# main worktime counter
class MainApp():
	def __init__(self):
		# installation path
		self.inspath = '/home/jin/projects/worklog/'
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
			
	# add client page
	def add_worktime(self):
		c = CounterManage()
		clientslisting = c.clisting()
		session.pop('clientid', None)
		return render_template('step1.htm', clientlist=clientslisting,savestatus="",savestatusclass="hidden")
		
	# main start window
	def client_selected(self):
		error = None
		a = AdditionalTools()
		# take client id from post
		clientid = request.form['client_sel']
		# find out the files basing on selected client
		inifile = "%s/db/%s.ini" % (self.inspath, clientid)
		csvfile = "%s/db/%s.csv" % (self.inspath, clientid)
		htmlpath = "%s/db/%s.html" % (self.inspath, clientid)
		htmlfile = "%s/%s.html" % (self.inspath, clientid)
		# read configs
		config.read(inifile)
		rconfig.read(inifile)
		# set up some variables
		curr = config.get("global", "currency")
		rate = int(config.get("money", curr))
		total_time = config.get("time", "total")
		total_time_human = a.time_human(int(total_time))
		total_time_hours = a.time_hours(int(total_time))
		tbutton='start'
		tbutton_class='btn-primary'
		note_class = 'hidden'
		status_class = 'hidden'
		# count total monies
		total_rate = total_time_hours * rate
		monies = int(total_rate)
		# count this month monies
		month_work_time = a.this_month(clientid)
		month_work_human = a.time_human(int(month_work_time))
		month_work_hours = a.time_hours(month_work_time)
		month_monies = int(month_work_hours) * rate
		# store variables in session
		session['clientid'] = clientid
		session['inifile'] = inifile
		session['csvfile'] = csvfile
		session['currency'] = curr
		session['rate'] = rate
		session['total_time'] = total_time
		session['total_time_human'] = total_time_human
		session['total_time_hours'] = total_time_hours
		session['month_work_human'] = month_work_human
		session['monies'] = monies
		session['month_monies'] = month_monies
		# get work history
		work_details = a.show_history()
		# render page
		return render_template('logger.htm', currency=curr,rate=rate,total_time=total_time,clientid=clientid,tbutton=tbutton,tbutton_class=tbutton_class,note_class=note_class,work_details=work_details,time_human=total_time_human,monies=monies,month_time=month_work_human,month_monies=month_monies,status_class=status_class)
	
	# counter start
	def start_counting(self):
		error = None
		a = AdditionalTools()
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
		# get work history
		work_details = a.show_history()
		return render_template('logger.htm', currency=self.curr,rate=self.rate,total_time=self.total_time,clientid=self.clientid,start_time=startt,stop_time=finisht,tbutton=tbutton,tbutton_class=tbutton_class,note_class=note_class,work_details=work_details,time_human=self.total_time_human,monies=self.monies,status_class=status_class,month_time=self.month_work_human,month_monies=self.month_monies)	

	# counter stop
	def stop_counting(self):
		a = AdditionalTools()
		# read configs
		config.read(self.inifile)
		rconfig.read(self.inifile)
		# read current total_time from config
		total_time = config.get("time", "total")
		# note the work finish time
		finish = datetime.datetime.now()
		finisht=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		# count the worktime
		delta = finish - self.start
		work_time=str(datetime.timedelta(seconds=delta.seconds))
		# count new total time
		new_total_time = int(total_time) + delta.seconds
		# get work note from input
		note = request.form['worknote']
		# open config and write new total time
		cfgfile= open(self.inifile,'w')
		rconfig.set("time", "total", new_total_time)
		rconfig.write(cfgfile)
		cfgfile.close()
		# put total time in a human way
		total_time_human = a.time_human(new_total_time)
		total_time_hours = a.time_hours(new_total_time)
		# count total monies
		total_rate = total_time_hours * self.rate
		monies = int(total_rate)
		# save worklog entry in worklog
		with open(self.csvfile, 'a') as csvlog:
			worklogwriter = csv.writer(csvlog, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			worklogwriter.writerow([self.startt, finisht, work_time, note])
		input_file = csv.DictReader(open(self.csvfile))
		work_start_var,work_stop_var,work_time_var,work_note_var = [],[],[],[] 	
		# put some variables for page rendering
		tbutton='start'
		tbutton_class='btn-primary'
		note_class='hidden'
		status_class=''
		# send data to session
		session['total_time'] = new_total_time
		# get work history
		work_details = a.show_history()
		# render page
		return render_template('logger.htm', currency=self.curr,rate=self.rate,total_time=new_total_time,clientid=self.clientid,start_time=self.startt,stop_time=finisht,tbutton=tbutton,tbutton_class=tbutton_class,note_class=note_class,work_details=work_details,time_human=total_time_human,monies=monies,status_class=status_class,month_time=self.month_work_human,month_monies=self.month_monies)

# some additional tools
class AdditionalTools():
	def __init__(self):
		self.inspath = '/home/jin/projects/worklog/'
	# add client function
	def client_add(self):
		error = None
		a = AdditionalTools()
		clientslisting = a.clisting()
		if request.method == 'POST':
			# check post message
			newclient = request.form['newclient']
			# put post variable into some other variables
			csvfile = "%s.csv" % newclient
			inifile = "%s.ini" % newclient		
			# create files
			os.system("cp %s/db_templates/template.csv %s/db/%s" % (self.inspath, self.inspath, csvfile))
			os.system("cp %s/db_templates/template.ini %s/db/%s" % (self.inspath, self.inspath, inifile))
			# render success page
			return render_template('step1.htm', clientlist=clientslisting,savestatus="Saved properly!",savestatusclass="alert alert-success")
		else:
			return "error"
			
	# time parsers
	def time_human(self,time):
		return str(datetime.timedelta(seconds=time))
	def time_hours(self,time):
		return (float(time) / 60)/60
		
	# show work history function
	def show_history(self):
		if 'clientid' in session:
			clientid = session['clientid']
		else:
			clientid = 0
		inifile = "%s/db/%s.ini" % (self.inspath, clientid)
		csvfile = "%s/db/%s.csv" % (self.inspath, clientid)
		htmlpath = "%s/db/%s.html" % (self.inspath, clientid)
		htmlfile = "%s/%s.html" % (self.inspath, clientid)
		input_file = csv.DictReader(open(csvfile))
		work_details = []
		for row in input_file:
			an_item = dict(dstart=row["date_start"],dend=row["date_stop"],dtime=row["work_time"],dnote=row["note"])
			work_details.append(an_item)
		return work_details
		
	# give this month money and time
	def this_month(self,clientid):
		a = AdditionalTools()
		csvfile = "%s/db/%s.csv" % (self.inspath, clientid)		
		input_file = csv.DictReader(open(csvfile))
		work_this_month = []
		work_month_time = 0
		month_now = str(datetime.datetime.now().strftime("%m"))
		for row in input_file:
			an_item = dict(dstart=row["date_start"],dend=row["date_stop"],dtime=row["work_time"],dnote=row["note"])
			row_date = datetime.datetime.strptime(row["date_start"], "%Y-%m-%d %H:%M:%S")
			row_date_end = datetime.datetime.strptime(row["date_stop"], "%Y-%m-%d %H:%M:%S")
			row_month = row_date.strftime("%m")
			# count the worktime
			delta_month = row_date_end - row_date
			row_work_time=str(datetime.timedelta(seconds=delta_month.seconds))
			if month_now == row_month:
				work_month_time = int(work_month_time) + delta_month.seconds
		work_month_human = int(work_month_time)
		return work_month_human
	
	# list clients
	def clisting(self):
		csvfiles = glob.glob('%s/db/*.csv' % self.inspath)
		csvlisting = [os.path.basename(x) for x in csvfiles]
		clientslisting = [remove_extension(s) for s in csvlisting]
		return clientslisting
		
# Pages routing
@app.route('/')
def welcome():
	m = MainApp()
	return m.add_worktime()

@app.route('/counter', methods=['POST'])		
def appready():
	m = MainApp()
	return m.client_selected()
	
@app.route('/count-start', methods=['POST'])		
def startcounter():
	m = MainApp()
	return m.start_counting()	
	
@app.route('/count-stop', methods=['POST'])
def stopcounter():
	m = MainApp()
	return m.stop_counting()
	
@app.route('/addclient', methods=['POST', 'GET'])
def addclient():
	a = AdditionalTools()
	return a.client_add()

# Start up flask
if __name__ == '__main__':
	app.secret_key = 'A0ZrSDA0cvasJC!Wa9cAXCn44AD!@'
	app.debug = True
	app.run(host='0.0.0.0')
