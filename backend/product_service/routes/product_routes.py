from flask import Blueprint, request, jsonify
from ..models import Product
from ..database import db

products = Blueprint('products', __name__)

@products.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])