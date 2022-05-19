from flask import Flask
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads,IMAGES

from flask_login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
photos =UploadSet('photos',IMAGES)

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])
    
    #photo uploads config
    app.config['UPLOADED_PHOTOS_DEST'] ='app/static/photos'
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
    # app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
    #configure uploadset
    configure_uploads(app,photos)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')
    
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    return app