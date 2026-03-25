from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

#Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)


@app.route("/")
def hello_world():
    return 'Hello World'


@app.route("/api/products/add", methods=["POST"])
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"],price=data["price"],description=data.get('description', ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added sucessfully"})
    return jsonify({"message": "Invalid product data"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)