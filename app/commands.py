from flask.cli import with_appcontext

from . import db
from .models import User, Question, Answer


@with_appcontext
def create_tables():
    db.create_all()