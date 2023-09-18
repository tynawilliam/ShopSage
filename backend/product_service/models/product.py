from datetime import datetime
import uuid
from ..database import db
from .category import Category


class Product(db.Model):
    __tablename__='products'

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, default=0, nullable=False)
    manufacturer = db.Column(db.String(255))
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    images = db.relationship('ProductImage', back_populates='product', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def serialize(self):
        return {
            'id' : self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock_quantity': self.stock_quantity,
            'manufacturer': self.manufacturer,
            'category_id': self.category_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'images': [img.serialize() for img in self.images]
        }