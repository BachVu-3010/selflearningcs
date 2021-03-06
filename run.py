#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
from app import create_app, db 
from flask_migrate import Migrate


# app = create_app(os.getenv("FLASK_CONFIG") or "default")
app = create_app("heroku")
migrate = Migrate(app, db)
