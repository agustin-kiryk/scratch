from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from src.config.mongodb import mongo
import os
from src.routes.auth import register_blueprint, auth_blueprint

load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Clave secreta para firmar los JWT

mongo.init_app(app)
jwt = JWTManager(app)


@app.route('/')
def index():
    return 'Hello world'


app.register_blueprint(register_blueprint, url_prefix='/user')
app.register_blueprint(auth_blueprint, url_prefix='/auth')


if __name__ == '__main__':
    app.run(debug=True)
