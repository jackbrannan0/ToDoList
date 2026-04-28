from app import app,db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, jsonify, url_for,redirect
from flask_login import LoginManager, current_user, login_required, login_user, logout_user



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
    

@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def index(): 
    from app.models import Task
    Task.query.all()        
    tasks = Task.query.filter_by(completed=False, user_id=current_user.id).all()
    completed_tasks = Task.query.filter_by(completed=True, user_id=current_user.id).all()
    return render_template("index.html", tasks=tasks, completed_tasks=completed_tasks) 


@app.route('/add', methods=['POST'])
@login_required
def add_task(): 
    from app.models import Task
    content = request.form.get('new_task')
    if content:
        task_add = Task(content=content, user_id=current_user.id)
        db.session.add(task_add)
        db.session.commit()
        return jsonify({"status":"success","message": "Added"})
    else:
        return jsonify({"status":"failure","message":"Unable to add" })


@app.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_tasks(task_id): 
    from app.models import Task
    task_to_delete = Task.query.get(task_id)
    if task_to_delete.user_id == current_user.id:
        db.session.delete(task_to_delete)
        db.session.commit()
        return jsonify({"status": "success", "message": "Deleted"})  
    else:
        return "Unauthorized", 403
   
     
    


@app.route('/complete/<int:task_id>', methods=['POST'])
@login_required
def complete_tasks(task_id): 
    from app.models import Task
    task = Task.query.get(task_id)
    if task.user_id == current_user.id:
        task.completed = True
        db.session.commit()
        return jsonify({"status": "success", "message": "Completed"}) 
    else:
        return "Unauthorized", 403









@app.route('/uncomplete/<int:task_id>', methods=['POST'])
@login_required
def uncomplete_tasks(task_id): 
    from app.models import Task
    task = Task.query.get(task_id)
    if task.user_id == current_user.id:
        task.completed = False
        db.session.commit()
        return jsonify({"status": "success", "message": "Uncompleted"}) 
    else:
        return "Unauthorized", 403










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
            login_user(new_user)
            return redirect(url_for('index')) 

    return render_template('register.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    from app.models import User
    if request.method == 'POST':
        username = request.form.get('username')
        password_attempt = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password_attempt):
         
            login_user(user)
            return redirect(url_for('index'))
        else:
           
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')









@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login')) 