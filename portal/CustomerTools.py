import datetime
import ConfigParser
import csv
import os
import re
import sys
import glob
from flask import Flask
from flask import render_template
from flask import request
from flask import session
import FileOperators
import AdditionalTools
class CustomerTools():	
	def login_page(self):
		return render_template('login.htm')
	def authentication(self):
		clientid = request.form['client_login']
		password = request.form['client_pass']
		return "OK"
