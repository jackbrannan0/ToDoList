from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

import os
import secrets



app = Flask(__name__) # Flask instance

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)



app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
print(app.secret_key) # Key needed for flask pop-up messages

@app.route('/') # base path

def index(): # Gets completed and non completed tasks from the database
    Task.query.all()        
    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template("index.html", tasks=tasks, completed_tasks=completed_tasks) # allows flask to render index.html and import task list


@app.route('/add', methods=['POST'])

def add_task(): # add tasks to database function
    content = request.form.get('new_task')
    if content:
        task_add = Task(content=content)
        db.session.add(task_add)
        db.session.commit()
        return jsonify({"status":"success","message": "Added"})
    else:
        return jsonify({"status":"failure","message":"Unable to add" })


# Add a new route to handle task deletion
@app.route('/delete/<int:task_id>', methods=['POST'])

def delete_tasks(task_id): # delete tasks from database
    task_to_delete = Task.query.get(task_id)
    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
        return jsonify({"status": "success", "message": "Deleted"})  
    else:
        return jsonify({"status":"failure","message":"Unable to delete" })
   
     
    
    
@app.route('/complete/<int:task_id>', methods=['POST'])

def complete_tasks(task_id): # complete task function - sends to db
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        db.session.commit()
        return jsonify({"status": "success", "message": "Completed"}) 
    else:
        return jsonify({"status":"failure","message":"Unable to complete" })

        
  
    


@app.route('/uncomplete/<int:task_id>', methods=['POST'])

def uncomplete_tasks(task_id): # function to uncomplete task
    task = Task.query.get(task_id)
    if task:
        task.completed = False
        db.session.commit()
        return jsonify({"status": "success", "message": "Uncompleted"}) 
    else:
        return jsonify({"status":"failure","message":"Unable to revert" })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True) 
