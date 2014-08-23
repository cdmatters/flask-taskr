#views.py
#

###################
##### imports #####
###################

from flask import Flask, flash, redirect, render_template,\
                request, session, url_for
from functools import wraps
from forms import AddTaskForm, RegisterForm, LoginForm
from flask.ext.sqlalchemy import SQLAlchemy


##################
##### config #####
##################

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from models import Task, User


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Plz login, pal.')
            return redirect(url_for('login'))
    return wrap


##################
### decorators ###
##################

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You logged out. Good'un!")
    return redirect(url_for('login'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        print form.errors
        if form.validate_on_submit():
            new_user = User(
                form.name.data, 
                form.email.data,
                form.password.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash('New user added! Woohoo!')
            return redirect(url_for('login'))
        else:
            flash("validation fail")
            print form.errors
            return render_template('register.html', form=form, error=error)
    if request.method == 'GET':
        return render_template('register.html', form=form)



@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            u = User.query.filter_by(
                name=request.form['name'],
                password=request.form['password']
                ).first()
            if u == None:
                error = ("Invalid username or password.")
            else:
                session['logged_in'] = True
                flash('You in mate. Knock yaself out')
                return redirect(url_for('tasks'))
        else:
            print form.errors
            return render_template('login.html', form=form, error=error)        

    if request.method == 'GET':
        return render_template("login.html", form=form, error=error)


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















