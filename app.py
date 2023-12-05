from flask import Flask, redirect, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model): # to create model
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) # set nullable=False bc we don't want the user to create a new task and then leave the content of task empty.
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id # everytime we make a new element, it's just going to return task and the ID of the task that has just been created. 

# with app.app_context():
#     db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] # request.form['content] - refer to index.html -> from form action -> and then pass in ID of input that we want to get the contents of which was 'content' AKA task_content is equal to the column beside 'Add Task'.
    #if we submit form, it will show this, otherwise, it's going to show our page - index.html
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task) # add new_task to database
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task.'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all() # this means that this is going to look at all of our database contents & query our database/ordering them by date created - newest to oldest and then grab all tasks. This is going to display all current tasks in table. 
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>') # /delete/<int:id> = to get the id of the content that needs to be deleted.
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) # This is going to get the task by ID. If it doesn't exist, it will return 404.

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task.'

@app.route('/update/<int:id>', methods=['GET', 'POST']) #/update/<int:id> = to get the id of the content that needs to be updated.
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