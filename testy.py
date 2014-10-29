#!/usr/bin/python
import datetime
import ConfigParser
import csv
import os
import re
import argparse
import sys
import glob
from mako.template import Template
config = ConfigParser.ConfigParser()
rconfig = ConfigParser.RawConfigParser()
global_config = "/etc/worklog_global.ini"
config.read(global_config)
rconfig.read(global_config)
wwwpath = config.get("main", "www_path")
inspath = config.get("main", "install_path")


os.system("cd %s" % inspath)
os.system("cd %s/db && ls *.csv |sed -e 's/\..*$//'" % inspath)

def remove_extension(s):
    return s[0:-4]

clients = glob.glob('%s/db/*.csv' % inspath)
clientslist = [os.path.basename(x) for x in clients]
clientslisting = [remove_extension(s) for s in clientslist]
print clientslist
print clientslisting
