from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'project-tracker-secret-key'

def get_db():
    conn = sqlite3.connect('/app/projects.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TEXT
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            title TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TEXT
        )''')
        conn.commit()

init_db()

@app.route('/')
def index():
    with get_db() as conn:
        projects = conn.execute('SELECT * FROM projects').fetchall()
    return render_template('index.html', projects=projects)

@app.route('/project/<int:project_id>')
def project_detail(project_id):
    with get_db() as conn:
        project = conn.execute('SELECT * FROM projects WHERE id=?', (project_id,)).fetchone()
        tasks = conn.execute('SELECT * FROM tasks WHERE project_id=?', (project_id,)).fetchall()
    return render_template('project.html', project=project, tasks=tasks)

@app.route('/create_project', methods=['POST'])
def create_project():
    name = request.form['name']
    desc = request.form.get('description', '')
    with get_db() as conn:
        conn.execute('INSERT INTO projects (name, description, created_at) VALUES (?, ?, ?)',
                     (name, desc, datetime.now().strftime('%Y-%m-%d %H:%M')))
        conn.commit()
    flash('Project created successfully!')
    return redirect(url_for('index'))

@app.route('/add_task/<int:project_id>', methods=['POST'])
def add_task(project_id):
    title = request.form['title']
    with get_db() as conn:
        conn.execute('INSERT INTO tasks (project_id, title, created_at) VALUES (?, ?, ?)',
                     (project_id, title, datetime.now().strftime('%Y-%m-%d %H:%M')))
        conn.commit()
    flash('Task added!')
    return redirect(url_for('project_detail', project_id=project_id))

@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    with get_db() as conn:
        conn.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task_id,))
        conn.commit()
    flash('Task marked as completed!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
