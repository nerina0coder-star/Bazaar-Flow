import socketio
from flask import Flask, render_template
from flask_socketio import SocketIO
from .config import config
from .extensions import db, login_manager, socket_io
from .blueprints.auth import auth_bp
from .blueprints.profile import profile_bp
from .blueprints.main import main_bp
from .blueprints.chamber import chamber_bp

def create_app(config_name='default'):

    # Initialize App
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    # Optionally load instance config
    app.config.from_pyfile('app.cfg', silent=True)

    # Initializing socketio app
    socket_io.init_app(app)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # starting db

    with app.app_context():
        db.create_all()

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(main_bp, url_prefix='/main')
    app.register_blueprint(chamber_bp, url_prefix='/chamber')

    # Simple home route
    @app.route('/')
    def home():
        return render_template("home.html")

    return socket_io, app