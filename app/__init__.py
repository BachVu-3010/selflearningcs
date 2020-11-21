#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_migrate import Migrate



import sys
# sys.path.append(
#     "c:\\Bach\\ComputerScience\\Fullstack_nanodegree\\QA_4anything\\database")




bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#



# Define an application factory function

def create_app():

    # static_folder='C:\Bach\ComputerScience\Fullstack_nanodegree\selflearningcs\app\static'
    # template_folder='C:\Bach\ComputerScience\Fullstack_nanodegree\selflearningcs\app\templates'

    # app = Flask(__name__,
    #     static_url_path= '', 
    #     static_folder = static_folder,
    #     template_folder = template_folder)



    app = Flask(__name__)

    
    app.config.from_object(config["development"])
    config["development"].init_app(app)

    # app.config.from_object(config.get(config_name))
    # config.get(config_name).init_app(app)



    # Set up bootstrap, moment, db at configuration time using the in_app method 
    # In this case all objects will be set up using the configuration values from FLask's current_app context global
    # This is useful if you have multiple applications running in the same process but with different configuration

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)



    # db = setup_db(app)
    migrate = Migrate(app, db)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    

    return app