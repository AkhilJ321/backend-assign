from enum import Enum
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, DataError
import datetime

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

# 1.Create a task
@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.json

        # Validate required fields
        required_fields = ['title', 'description', 'due_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Extract task details from the request data
        title = data['title']
        description = data['description']
        due_date = data['due_date']
        status = data.get('status', TaskStatus.INCOMPLETE.value)

        # Validate due_date format
        try:
            due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid due_date format. Use YYYY-MM-DD'}), 400

        # Create a new task and save it to the database
        new_task = Task(title=title, description=description, due_date=due_date, status=status)

        db.session.add(new_task)
        db.session.commit()

        return jsonify({'message': 'Task created successfully', 'task': new_task.id}), 201
    except IntegrityError:
        return jsonify({'error': 'Task already exists'}), 409
    except DataError:
        return jsonify({'error': 'Invalid data provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    # 2.Receive a task by its uid

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

# 3.Update an Existing Task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.json

        # Get the task from the database
        task = Task.query.get_or_404(task_id)

        # Validate required fields
        required_fields = ['title', 'description', 'due_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Update task details if provided in the request
        task.title = data['title']
        task.description = data['description']

        due_date = data['due_date']
        try:
            due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d').date()
            task.due_date = due_date
        except ValueError:
            return jsonify({'error': 'Invalid due_date format. Use YYYY-MM-DD'}), 400

        task.status = data.get('status', task.status)

        db.session.commit()

        return jsonify({'message': 'Task updated successfully'})
    except IntegrityError:
        return jsonify({'error': 'Task already exists'}), 409
    except DataError:
        return jsonify({'error': 'Invalid data provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 4.Delete a Task

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({'message': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200


# 5. List all task (pagination included)
@app.route('/tasks', methods=['GET'])
def list_tasks():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Validate page and per_page values
        if page < 1 or per_page < 1:
            return jsonify({'error': 'Invalid pagination parameters'}), 400

        tasks = Task.query.paginate(page=page, per_page=per_page)

        task_list = []
        for task in tasks.items:
            task_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date.strftime('%Y-%m-%d'),
                'status': task.status.value
            }
            task_list.append(task_data)

        return jsonify({
            'tasks': task_list,
            'page': tasks.page,
            'per_page': tasks.per_page,
            'total_pages': tasks.pages,
            'total_items': tasks.total
        })
    except ValueError:
        return jsonify({'error': 'Invalid pagination parameters'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
   
    app.run()
