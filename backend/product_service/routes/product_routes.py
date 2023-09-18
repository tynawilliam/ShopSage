from flask import Blueprint, request, jsonify
from ..models import Product, ProductImage
from ..database import db

products = Blueprint('products', __name__)

@products.route('/', methods=['POST'])
def new_product():
    try:
        data = request.get_json()
        add_product = Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            stock_quantity=data['stock_quantity'],
            manufacturer=data['manufacturer'],
            category_id=data['category_id'],
        )
        db.session.add(add_product)

        image_urls = data.get('image_urls',[])
        for url in image_urls:
            image = ProductImage(image_url=url)
            add_product.images.append(image)


        db.session.commit()
        return jsonify({'message' : 'Product Added' }),201
    except Exception as e:
        return jsonify({'message' : str(e)}), 500

@products.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])