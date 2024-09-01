import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)
    
    from .models import Task, Status
    create_db(app)
    register_cli(app, db)

    return app

def create_db(app: Flask):
    with app.app_context():
        db.create_all()
        
def register_cli(app: Flask, db: SQLAlchemy):
    from .models import Task, Status

    @app.cli.command('add')
    @click.argument('description', type=str)
    def add(description):
        task = Task(description=description, 
                    status_id=Status.query.filter_by(description='todo').first().id
        )
        db.session.add(task)
        db.session.commit()
        click.echo(f'Task added successfully (ID: {task.id})')
        
    @app.cli.command('update')
    @click.argument('task_id')
    @click.argument('description')
    def update(task_id, description):
        task = Task.query.get(task_id)
        task.description = description
        db.session.commit()
        click.echo(f'Task updated successfully (ID: {task.id})')
        
    @app.cli.command('delete')
    @click.argument('task_id')
    def delete(task_id):
        task = Task.query.get(task_id)
        db.session.delete(task)
        db.session.commit()
        click.echo(f'Task deleted successfully (ID: {task.id})')
        
    @app.cli.command('mark-in-progress')
    @click.argument('task_id')
    def mark_in_progress(task_id):
        task = Task.query.get(task_id)
        task.status_id = Status.query.filter_by(description='in-progress').first().id
        db.session.commit()
        click.echo(f'Task marked as in progress (ID: {task.id})')
        
    @app.cli.command('mark-done')
    @click.argument('task_id')
    def mark_done(task_id):
        task = Task.query.get(task_id)
        task.status_id = Status.query.filter_by(description='done').first().id
        db.session.commit()
        click.echo(f'Task marked as done (ID: {task.id})')
        
    @app.cli.command('list')
    @click.option('-s', '--status', default=None)
    def list(status):
        tasks = Task.query.all()
        if not status:
            for task in tasks:
                status_obj = Status.query.get(task.status_id)
                click.echo(f'{task.id}: {task.description} ({status_obj.description})')
        else:
            status_obj = Status.query.filter_by(description=status).first()
            for task in tasks:
                if task.status_id == status_obj.id:
                    click.echo(f'{task.id}: {task.description} ({status_obj.description})')
                    
    @app.cli.command('seed')
    def seed():
        from .seeders import seed_statuses
        seed_statuses()
        click.echo('Seed data added successfully')