from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-for-project-tracker'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Project Model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='In Progress')
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Project {self.name}>'

# Create DB tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

@app.route('/add', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description')
        status = request.form.get('status', 'In Progress')
        
        new_project = Project(name=name, description=description, status=status)
        db.session.add(new_project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('project.html', title="Add New Project")

@app.route('/project/<int:project_id>')
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project.html', title="Project Details", project=project, view_mode=True)

@app.route('/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form.get('description')
        project.status = request.form.get('status')
        if request.form.get('end_date'):
            project.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('project.html', title="Edit Project", project=project)

@app.route('/delete/<int:project_id>')
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)