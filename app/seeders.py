from .models import Status
from . import db

def seed_statuses():
    statuses = ['todo', 'in-progress', 'done']
    for status in statuses:
        db.session.add(Status(description=status))
    db.session.commit()