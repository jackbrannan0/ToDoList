from flask import Flask, render_template, request, redirect#importing Flask
import sqlite3



def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)')
        print("Database initialised!")
        try:
            conn.execute('ALTER TABLE tasks ADD COLUMN completed BOOLEAN DEFAULT 0')
        except sqlite3.OperationalError:
            print("Column already exists!")    

init_db()        


app = Flask(__name__) # Flask instance

my_tasks = ['Buy Food', 'Do Coding', 'Walk Dog'] # Task List




@app.route('/') # base path

def index():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        
    return render_template("index.html", tasks=tasks) # allows flask to render index.html and import task list


@app.route('/add', methods=['POST'])

def add_task():
    content = request.form.get('new_task')
    if content:
        with sqlite3.connect('database.db') as conn:
            conn.execute('INSERT INTO tasks (content) VALUES (?)',(content,))
            conn.commit()
            
    return redirect('/')

        


# Add a new route to handle task deletion
@app.route('/delete/<int:task_id>', methods=['POST'])

def delete_tasks(task_id):
    with sqlite3.connect('database.db') as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
    return redirect('/')    
    
    



if __name__ == "__main__":
    app.run(debug=True) 
