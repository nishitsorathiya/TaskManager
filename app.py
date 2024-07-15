# Import flask framework, template loader and internal objects
from flask import Flask, render_template, request, redirect
# Import sqlalchemy (database library) plugin for flask
from flask_sqlalchemy import SQLAlchemy
# Import datetime library for working with date
from datetime import datetime

# Create flask object
app = Flask(__name__)
# Set database path in flask application config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# Create database object inside flask application's internal context/memory
with app.app_context():
    db = SQLAlchemy(app)

# Create class for todo list which is a child class of sqlalchemy's database model class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

    def _repr_(self):
        return '<Task %r>' % self.id

# Create a default/root route which accepts POST and GET requests
    
@app.route('/', methods=['POST', 'GET'])
def index():
    # If POST request is received, get data of content form and create a task by creating object of Todo class
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        # Add created object to database else throw error
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.data_created).all()
        return render_template('index.html', tasks=tasks)

# Method for deleting todolist task


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')

    except:
        return 'There was a problem deleting that task'

# Method for updating todolist task


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)