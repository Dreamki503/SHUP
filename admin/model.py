from config import db
from datetime import datetime

class category_category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(50), unique = True)
    slug = db.Column(db.String(100), unique = True)

class store_product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String(200))
    slug = db.Column(db.String(200))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    images = db.Column(db.String(100))
    stock = db.Column(db.Integer)
    is_available = db.Column(db.SmallInteger)
    created_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category_category.id'), nullable = False)

    category = db.relationship('category_category', backref = db.backref('poducts', lazy = True))

class orders_order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    order_number = db.Column(db.String(20), nullable = False)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(15), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    address_line_1 = db.Column(db.String(50), nullable = False)
    address_line_2 = db.Column(db.String(50), nullable = False)
    state = db.Column(db.String(50), nullable = False)
    city = db.Column(db.String(50), nullable = False)
    order_total = db.Column(db.Double, nullable = False)
    tax = db.Column(db.Double, nullable = False)
    status = db.Column(db.String(10), nullable = False)
    ip = db.Column(db.String(20), nullable = False)
    is_ordered = db.Column(db.SmallInteger, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False)
    updated_at = db.Column(db.DateTime, nullable = False)
    user_id = db.Column(db.Integer)
    payment_id = db.Column(db.Integer)
    