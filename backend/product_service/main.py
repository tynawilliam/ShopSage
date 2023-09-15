from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from .database import db
from .config import Config
from .models.product import Product
from .models.category import Category
from .models.product_image import ProductImage

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    return 'Hello, World!'
