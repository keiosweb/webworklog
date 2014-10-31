import datetime
import ConfigParser
import csv
import os
import re
import sys
import glob
from portal import app
from flask import Flask
from flask import render_template
from flask import request, session, redirect, url_for
import FileOperators
import MainApp
import AdditionalTools
import CustomerTools
from models import db, User, Customer
from forms import SignupForm,CreateForm,SigninForm

# Pages routing
@app.route('/counter', methods=['POST'])
def show_worklog():
	m = MainApp.BackendMainPage()
	return m.main_page()

@app.route('/')
def admin_login():
	m = MainApp.MainApp()
	return m.add_worktime()

@app.route('/count-start', methods=['POST'])		
def admin_counterstart():
	m = MainApp.WorkCounter()
	return m.start_counting()	
	
@app.route('/count-stop', methods=['POST'])
def admin_counterstop():
	m = MainApp.WorkCounter()
	return m.stop_counting()


@app.route('/backend')
def client_selector():
	m = MainApp.ClientsManage()
	return m.list_clients()

@app.route('/create', methods=['GET', 'POST'])
def customer_create():
  form = CreateForm()
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.htm', form=form)
    else:
      newclient = Customer(form.clientid.data, form.firstname.data, form.lastname.data, form.email.data)
      db.session.add(newclient)
      db.session.commit()
      return "ALL OK"
  elif request.method == 'GET':
    return render_template('create.htm', form=form)

@app.route('/panel')
def profile():
	if 'email' not in session:
		return redirect(url_for('signin'))
	user = User.query.filter_by(email = session['email']).first()
	if user is None:
		return redirect(url_for('signin'))
	else:
		return render_template('profile.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.htm', form=form)
    else:
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()
      session['email'] = newuser.email
      return redirect(url_for('panel'))
   
  elif request.method == 'GET':
    return render_template('signup.htm', form=form)

@app.route('/customer', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('login.htm', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('login.htm', form=form)
