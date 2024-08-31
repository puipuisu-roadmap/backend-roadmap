from datetime import datetime
from . import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    
class Status(db.Model):
    __tablename__ = 'statuses'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    