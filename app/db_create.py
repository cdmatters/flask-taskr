#db_create.py
# This file creates a database used for the task manager
# It is clear we will need fields for NAME, DUE DATE, PRIORITY, STATUS, ID

from views import db
from models import Task
from datetime import date

db.create_all()

db.session.add(Task("Finish this tutorial", date(2014, 8, 23), 10, 1))
db.session.add(Task("Finish Real Python", date(2014, 9, 1), 10, 1))
db.session.commit()

