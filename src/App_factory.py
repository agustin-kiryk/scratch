from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from src.config.mongodb import mongo
from src.config.Email_config import Config
from src.routes.register import register_bp

mail = Mail()


def create_app():
    app = Flask(__name__)
    app.json.sort_keys = False
    app.config.from_object(Config)

    # Inicialización de Flask-Mail
    mail.init_app(app)

    mongo.init_app(app)
    jwt = JWTManager(app)

    from src.routes.auth import register_blueprint, auth_blueprint
    app.register_blueprint(register_blueprint, url_prefix='/user')
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(register_bp, url_prefix='/api')

    from src.routes.Webhook_paycaddy import webhook_paycaddy_blueprint
    app.register_blueprint(webhook_paycaddy_blueprint, url_prefix='/webhook')
    
    from src.routes.FinancialInfoRoute import financial_bp
    app.register_blueprint(financial_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return 'Hello world umpi penw tftf pxjl'

    return app
