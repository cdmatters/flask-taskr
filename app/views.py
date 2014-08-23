#views.py
#


from flask import Flask, flash, redirect, render_template,\
                request, session, url_for, g
from functools import wraps
from forms import AddTaskForm
import sqlite3


app = Flask(__name__)
app.config.from_object('config')


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


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
    g.db = connect_db()
    cur= g.db.execute(
        'SELECT name, due_date, priority, task_id FROM tasks WHERE status=1'
        )
    open_tasks = []
    for row in cur.fetchall():
        open_tasks.append(dict(name=row[0], due_date=row[1],
                                priority=row[2], task_id=row[3]))

    cur= g.db.execute(
        'SELECT name, due_date, priority, task_id FROM tasks WHERE status=0'
        )

    closed_tasks = []
    for row in cur.fetchall():
        closed_tasks.append(dict(name=row[0], due_date=row[1],
                                priority=row[2], task_id=row[3]))

    g.db.close()

    return render_template(
        'tasks.html',
        form=AddTaskForm(request.form),
        open_tasks =open_tasks,
        closed_tasks = closed_tasks
    )


@app.route('/add/', methods=['POST'])
@login_required
def new_task():
    g.db = connect_db()
    name = request.form['name']
    date = request.form['due_date']
    priority = request.form['priority']
    if not name or not date or not priority:
        flash('Please fill in all fields')
        return redirect(url_for('tasks'))
    else:
        cur = g.db.execute("INSERT INTO tasks ('name', 'due_date', \
        'priority', 'status') VALUES(?, ?, ?, 1 )",
        (name, date, priority))
        g.db.commit()
        g.db.close()
        flash('New entry posted! Good job! Thanks.')
        return redirect(url_for('tasks'))


@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
    g.db = connect_db()
    g.db.execute(
        'UPDATE tasks SET status=0 WHERE task_id='+str(task_id)
        )
    g.db.commit()
    g.db.close()
    flash('The task was marked as complete')
    return redirect(url_for('tasks'))


@app.route('/delete/<int:task_id>')
@login_required 
def delete_entry(task_id):
    g.db = connect_db()
    g.db.execute('DELETE FROM tasks WHERE task_id='+str(task_id))
    g.db.commit()
    g.db.close()
    flash('The task was deleted.')
    return redirect(url_for('tasks'))














