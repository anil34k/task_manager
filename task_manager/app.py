from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Connection Configuration
def create_connection():
    conn = mysql.connector.connect(
        host='localhost',
        database='task_manager_db',
        user='root',
        password='ANIL@0707'  # Replace with your MySQL root password
    )
    return conn

# Route to display all tasks
@app.route('/')
def index():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description) VALUES (%s, %s)", (title, description))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('index'))

# Route to edit an existing task
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        
        cursor.execute("UPDATE tasks SET title=%s, description=%s WHERE id=%s", (title, description, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.execute("SELECT * FROM tasks WHERE id=%s", (id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return render_template('edit.html', task=task)

# Route to delete a task
@app.route('/delete_task/<int:id>', methods=['POST'])
def delete_task(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
