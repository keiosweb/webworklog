import datetime
import ConfigParser
import csv
import os
import re
import sys
import glob
from flask import Flask
from flask import session
def remove_extension(s):
		return s[0:-4]
global_inspath = '/home/jin/projects/worklog/'
class FileOperators():
	def __init__(self):
		self.inspath = global_inspath
	def clisting(self):
		csvfiles = glob.glob('%s/db/*.csv' % self.inspath)
		csvlisting = [os.path.basename(x) for x in csvfiles]
		clientslisting = [remove_extension(s) for s in csvlisting]
		return clientslisting
	def cremove(self,clientid):
		os.system('rm -rf %s/%s.*' % (self.inspath, clientid))
