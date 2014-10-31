# some additional tools
import datetime
import ConfigParser
import csv
import os
import re
import sys
import glob

class AdditionalTools():		
	# time parsers
	def time_human(self,time):
		return str(datetime.timedelta(seconds=time))
	def time_hours(self,time):
		return (float(time) / 60)/60
