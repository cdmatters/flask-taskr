#config.py
# This module contains all the configurations for the start of the app

import os

# this grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
USERNAME = 'admin'
PASSWORD = 'admin'
CSRF_ENABLED = True
SECRET_KEY = "1c498a0b8b9d8151a4d81ecfcec702ec2d04b94188a995edeae68980b456157a153837\
d17b25c0156bc900270dfe2f06578ac7f0e933109fa944f0b08ff10d73f316e0217f80\
cff765ac91d6e6aa07e07dc269628838503c504944dacd8a89db400e928a798d6c1203\
37971b6180a584e04df46d8af778dcecc236eb94967dabdf2b2db4d22e73618feb7ec0\
2a889f632d29cc4ddeed5a240d90799a5e1e398ce1e2e097c565f4a2612e74f5666ecb\
f89eae96ca13c79188b82dbb64deb940696568e97d30b5745c9f4a9292f778bec08316\
3ffbcee59f0e7074a1364a564811fd9baf8d6f13dd0cdaf8f457afa37ca0fd3db7eef7\
eb9f03de08c3cff2445f9941fd6eb76a9b8d9ab755bd7aae14848556c641c09ff2ee77"

# defines the full path for the DATABASE
DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ DATABASE_PATH