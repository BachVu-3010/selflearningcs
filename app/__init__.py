#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#



from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager



# Create and initialize flask extension

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#



# Define an application factory function

def create_app(config_name = "default"):

    # static_folder='C:\Bach\ComputerScience\Fullstack_nanodegree\selflearningcs\app\static'
    # template_folder='C:\Bach\ComputerScience\Fullstack_nanodegree\selflearningcs\app\templates'

    # app = Flask(__name__,
    #     static_url_path= '', 
    #     static_folder = static_folder,
    #     template_folder = template_folder)

  

    app = Flask(__name__) 
    # app.config.from_object(config.get(config_name))
    # config.get(config_name).init_app(app)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)



    # Set up bootstrap, moment, db at configuration time using the in_app method 
    # In this case all objects will be set up using the configuration values from FLask's current_app context global
    # This is useful if you have multiple applications running in the same process but with different configuration

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # with app.app_context():
    #     db.create_all()

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint, url_prefix = '/')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    

    return app