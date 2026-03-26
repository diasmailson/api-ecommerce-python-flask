from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, login_user, logout_user, LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '$ecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

#Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

#Auth
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Routes
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()
    if user and data.get("password") == user.password:
        login_user(user)    
        print(user)
        return jsonify({"message": "Logged in sucessfully"})
    return jsonify({"message": "Unauthorized. Invalid credentials"}), 401

@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout sucessufully"})


@app.route("/api/products/add", methods=["POST"])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"],price=data["price"],description=data.get('description', ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added sucessfully"})
    return jsonify({"message": "Invalid product data"}), 400

@app.route("/api/products/delete/<int:product_id>", methods=["DELETE"])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted sucessfully"})
    return jsonify({"message":  "Product not found"}), 404

@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message":  "Product not found"}), 404

@app.route("/api/products/update/<int:product_id>", methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message":"Product not found"}), 404

    data = request.json
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'description' in data:
        product.description = data['description']

    db.session.commit()
    return jsonify({"message": "Product updated sucessfully"})

@app.route("/api/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_list.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description
        })
        
    return jsonify(product_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)