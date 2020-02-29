# Entry point for the app
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
# will set base dir to our files current dir
basedir = os.path.abspath(os.path.dirname(__file__))
# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# init db
db = SQLAlchemy(app)
# init Marshmallow
ma = Marshmallow(app)


"""
To create a DB:
    from app import db
    db.create_all()
"""


# prodcut class / model
class Product(db.Model):
    # assign fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    # constructor
    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty


# ProductSchema serializer
class ProductSchema(ma.Schema):
    class Meta:
        # show all fields
        fields = ('id', 'name', 'description', 'price', 'qty')


# Init schema
prodcut_schema = ProductSchema()  # singular product
products_schema = ProductSchema(many=True)  # many products


# create a product
@app.route('/product', methods=['POST'])
def add_product():
    # pull the name and other fields off the req obj
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_prodcut = Product(name, description, price, qty)
    db.session.add(new_prodcut)
    db.session.commit()

    return prodcut_schema.jsonify(new_prodcut)


# get all the products in the db
@app.route('/products', methods=["GET"])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    print("RESULT:\t", result)
    return jsonify(result)


# get a product from the DB
@app.route('/product/<id>', methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    print("RESULT:\t", product)
    return prodcut_schema.jsonify(product)


# update a product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)

    # pull the name and other fields off the req obj
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()

    return prodcut_schema.jsonify(product)


# delete product
@app.route('/product/<id>', methods=["DELETE"])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return prodcut_schema.jsonify(product)


@app.route('/', methods=['GET'])
def get():
    return jsonify({"msg": "Hello world"})


if __name__ == '__main__':
    app.run(debug=True)
