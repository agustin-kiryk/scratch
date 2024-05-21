from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from src.config.mongodb import mongo
from src.config.Email_config import Config

mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicialización de Flask-Mail
    mail.init_app(app)

    mongo.init_app(app)
    jwt = JWTManager(app)

    from src.routes.auth import register_blueprint, auth_blueprint
    app.register_blueprint(register_blueprint, url_prefix='/user')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    @app.route('/')
    def index():
        return 'Hello world'

    return app
