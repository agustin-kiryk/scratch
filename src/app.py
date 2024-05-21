from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from src.config.mongodb import mongo
import os
from src.routes.auth import register_blueprint, auth_blueprint
from flask_mail import Mail


load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Clave secreta para firmar los JWT

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS').lower() in ['true', '1', 'yes']
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL').lower() in ['true', '1', 'yes']

# Inicialización de Flask-Mail
mail = Mail(app)

mongo.init_app(app)
jwt = JWTManager(app)


@app.route('/')
def index():
    return 'Hello world'


app.register_blueprint(register_blueprint, url_prefix='/user')
app.register_blueprint(auth_blueprint, url_prefix='/auth')


if __name__ == '__main__':
    app.run(debug=True)
