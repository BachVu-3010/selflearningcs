#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
from app import create_app, db 
from app.models import Question, Answer
from flask_migrate import Migrate


app = create_app('development')
migrate = Migrate(app, db)
