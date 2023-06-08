from enum import Enum
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class TaskStatus(Enum):
    INCOMPLETE = 'incomplete'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.INCOMPLETE)

    def __repr__(self):
        return f'<Task {self.title}>'


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json

    # Extract task details from the request data
    title = data.get('title')
    description = data.get('description')
    due_date_str = data.get('due_date')
    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
    status = data.get('status', TaskStatus.INCOMPLETE.value)

    db.create_all()

    new_task = Task(title=title, description=description, due_date=due_date, status=status)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': 'Task created successfully', 'task': new_task.id}), 201

@app.route('/tasks/<int:task_id>',methods=['POST'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'message':'Task not found'}),404
    
    task_data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.strftime('%Y-%m-%d'),
        'status': task.status.value
    }

    return jsonify({'task': task_data}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'message': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json

    # Get the task from the database
    task = Task.query.get_or_404(task_id)

    # Update task details if provided in the request
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_date = data.get('due_date', task.due_date)
    task.status = data.get('status', task.status)

    # Save the changes to the database
    db.session.commit()

    return jsonify({'message': 'Task updated successfully'})


@app.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.query.all()

    task_list = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.strftime('%Y-%m-%d'),
            'status': task.status.value
        }
        task_list.append(task_data)

    return jsonify({'tasks': task_list})

if __name__ == '__main__':
   
    app.run()
