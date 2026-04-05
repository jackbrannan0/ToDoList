from app import app,db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, jsonify, url_for,redirect

# base path

@app.route('/tasks', methods=['GET', 'POST'])
def index(): # Gets completed and non completed tasks from the database
    from app.models import Task
    Task.query.all()        
    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template("index.html", tasks=tasks, completed_tasks=completed_tasks) # allows flask to render index.html and import task list


@app.route('/add', methods=['POST'])

def add_task(): # add tasks to database function
    from app.models import Task
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
    from app.models import Task
    task_to_delete = Task.query.get(task_id)
    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
        return jsonify({"status": "success", "message": "Deleted"})  
    else:
        return jsonify({"status":"failure","message":"Unable to delete" })
   
     
    
    
@app.route('/complete/<int:task_id>', methods=['POST'])

def complete_tasks(task_id): # complete task function - sends to db
    from app.models import Task
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        db.session.commit()
        return jsonify({"status": "success", "message": "Completed"}) 
    else:
        return jsonify({"status":"failure","message":"Unable to complete" })

@app.route('/uncomplete/<int:task_id>', methods=['POST'])

def uncomplete_tasks(task_id): # function to uncomplete task
    from app.models import Task
    task = Task.query.get(task_id)
    if task:
        task.completed = False
        db.session.commit()
        return jsonify({"status": "success", "message": "Uncompleted"}) 
    else:
        return jsonify({"status":"failure","message":"Unable to revert" })




@app.route('/', methods=['GET','POST']) 
def register():
    from app.models import User
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_value = generate_password_hash(password, method='pbkdf2:sha256')

        user = User.query.filter_by(username=username).first()

        
        if user:
            return render_template('register.html', error="User already exists")
        else:
            new_user = User(username=username, password_hash=hashed_value)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))  # redirect to login page

    return render_template('register.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    from app.models import User
    if request.method == 'POST':
        username = request.form.get('username')
        password_attempt = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        # check_password_hash handles the heavy lifting
        if user and check_password_hash(user.password_hash, password_attempt):
            # Success!
            return redirect(url_for('index'))
        else:
            # Failure
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')