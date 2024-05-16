from flask import Flask
from dotenv import load_dotenv
from src.config.mongodb import mongo
import os
from src.routes.register import register_blueprint

load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)


@app.route('/')
def index():
    return 'Hello world'


app.register_blueprint(register_blueprint, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)
