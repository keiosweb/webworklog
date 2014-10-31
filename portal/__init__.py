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
import MainApp
import AdditionalTools
import CustomerTools

# some initial things for whole app
app = Flask(__name__)
app.secret_key = 'A0ZrSDA0cvasJC!Wa9cAXCn44AD!@'
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://worklog:worklogpassword@localhost/worklog'
from models import db
db.init_app(app)
import portal.routes

