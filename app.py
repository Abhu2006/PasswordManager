from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///password_db.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(200), nullable=False)
    site_url = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return 'Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():

        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/add_account', methods=['POST', 'GET'])
def add_account():

    if request.method == 'POST':
        site = request.form['site']
        site_url = request.form['site_url']
        username = request.form['username']
        password = request.form['password']
        new_task = Todo(site=site, site_url=site_url, username=username, password=password)

        try:
            db.create_all()
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was some issue.Please try Again'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('add_account.html', task=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was some issue.Please try Again'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.site = request.form['site']
        task.site_url = request.form['site_url']
        task.username = request.form['username']
        task.password = request.form['password']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was some issue.Please try Again'
    else:
        return render_template('update.html', task=task)

@app.route('/show_pwd/<int:id>', methods=['POST', 'GET'])
def show_pwd(id):
    task = Todo.query.get_or_404(id)
    return render_template('show_pwd.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
