from flask import Blueprint, request, jsonify
from ..models import Product, ProductImage
from ..database import db

products = Blueprint('products', __name__)

def handle_product_images_update(product, new_image_urls):
    current_image_urls = [img.image_url for img in product.images]

    for url in new_image_urls:
        if url not in current_image_urls:
            new_image = ProductImage(image_url=url, product=product)
            db.session.add(new_image)

    for current_image in product.images:
        if current_image.image_url not in new_image_urls:
            db.session.delete(current_image)


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
def get_all_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])


@products.route("/<string:product_id>",methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product: 
            return jsonify({'message' : 'Product Not Found' }),404
        
        product_data=product.serialize()
        return jsonify(product_data), 200
    
    except Exception as e:
        return jsonify({'message' : str(e)}), 500


@products.route("/<string:product_id>",methods=['PUT'])
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product: 
            return jsonify({'message' : 'Product Not Found' }),404

        data = request.get_json()
        if 'name' in data:
            product.name = data['name']

        if 'description' in data:
            product.description = data['description']

        if 'price' in data:
            product.price = data['price']

        if 'stock_quantity' in data:
            product.stock_quantity = data['stock_quantity']

        if 'manufacturer' in data:
            product.manufacturer = data['manufacturer']

        if 'category_id' in data:
            product.category_id = data['category_id']

        if 'image_urls' in data:
            handle_product_images_update(product, data['image_urls'])

        db.session.commit()

        return jsonify({'message': 'Product updated successfully'}), 200


    except Exception as e:
        return jsonify({'message' : str(e)}), 500