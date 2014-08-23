#views.py
#


from flask import Flask, flash, redirect, render_template,\
                request, session, url_for, g
from functools import wraps
from forms import AddTaskForm
from flask.ext.sqlalchemy import SQLAlchemy

#COMMENTED OUT: old using SQLite3
#import sqlite3

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import Task


#COMMENTED OUT: old using SQLite3
#def connect_db():
#   return sqlite3.connect(app.config['DATABASE'])


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Plz login, pal.')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You logged out. Good'un!")
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] \
        or request.form['password'] != app.config['PASSWORD']:
            error = "Invalid Credentials. Try agin, bud."
            return render_template("login.html", error= error)

        else:
            session['logged_in'] = True
            return redirect(url_for('tasks'))
    if request.method == 'GET':
        return render_template("login.html")


@app.route('/tasks/')
@login_required
def tasks():
    open_tasks = db.session.query(Task) \
        .filter_by(status='1').order_by(Task.due_date.asc())
    closed_tasks = db.session.query(Task) \
        .filter_by(status='0').order_by(Task.due_date.asc())

    return render_template(
        'tasks.html',
        form=AddTaskForm(request.form),
        open_tasks = open_tasks,
        closed_tasks = closed_tasks
    )


@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    form = AddTaskForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_task = Task(
                form.name.data,
                form.due_date.data,
                form.priority.data,
                '1'
            )
            db.session.add(new_task)
            db.session.commit()
            flash('Nu entry dun dun dun. Well done.')
        else:
            flash('did not validate')
    return redirect(url_for('tasks'))


@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).update({"status":"0"})
    db.session.commit()
    flash('Task marked as complete. You go, Glen Coco.')
    return redirect(url_for('tasks'))


@app.route('/delete/<int:task_id>')
@login_required 
def delete_entry(task_id):
    new_id = task_id
    db.session.query(Task).filter_by(task_id=new_id).delete()
    db.session.commit()
    flash('The task was deleted.')
    return redirect(url_for('tasks'))















