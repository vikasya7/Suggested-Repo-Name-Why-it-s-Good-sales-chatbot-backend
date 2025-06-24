from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
import random

app = Flask(__name__)
CORS(app)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
faker = Faker()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    brand = db.Column(db.String(80))
    rating = db.Column(db.Float)
    image_url = db.Column(db.String(255))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)





users = []

@app.route('/')
def index():
    return "Backend API is running"

# @app.route("/init-db")
# def init_db():
#     db.drop_all()
#     db.create_all()

#     for _ in range(100):
#         product = Product(
#             name=faker.word().capitalize() + " " + faker.word().capitalize(),
#             price=random.randint(200, 5000),
#             description=faker.sentence(),
#             brand=faker.company(),
#             rating=round(random.uniform(3.0, 5.0), 1),
#             image_url="https://via.placeholder.com/150"
#         )
#         db.session.add(product)

#     db.session.commit()
#     return "Database initialized with enriched product data"


@app.route('/products', methods=["GET"])
def get_products():
    all_products = Product.query.all()
    return jsonify([
    {
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "description": p.description,
        "brand": p.brand,
        "rating": p.rating,
        "image_url": p.image_url
    } for p in all_products
])

@app.route("/preview-products")
def preview_products():
    products = Product.query.limit(20).all()
    return jsonify([p.name for p in products])

@app.route('/chatbot-query', methods=["POST"])
def chatbot_query():
    data = request.get_json()
    query = data.get("query", "").lower()

    matches = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    return jsonify([
        {"id": p.id, "name": p.name, "price": p.price} for p in matches
    ])

@app.route('/signup', methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Signup successful"})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({"message": "Login successful"})

    return jsonify({"error": "Invalid credentials"}), 401


if __name__ == "__main__":
    app.run(port=5001, debug=True)





