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
    db.drop_all()
    db.create_all()

    # ✅ 10 Realistic Products with Real Images
    fixed_products = [
        {
            "name": "Wireless Mouse",
            "price": 499,
            "description": "Ergonomic wireless mouse with smooth tracking and USB receiver.",
            "brand": "Logitech",
            "rating": 4.5,
            "image_url": "https://m.media-amazon.com/images/I/61LtuGzXeaL._SX679_.jpg"
        },
        {
            "name": "Gaming Keyboard",
            "price": 1499,
            "description": "Mechanical RGB keyboard with blue switches and metal frame.",
            "brand": "Redragon",
            "rating": 4.7,
            "image_url": "https://m.media-amazon.com/images/I/71cNGtGzTwL._SX679_.jpg"
        },
        {
            "name": "LED Desk Lamp",
            "price": 899,
            "description": "Foldable LED lamp with USB charging and adjustable brightness.",
            "brand": "Philips",
            "rating": 4.3,
            "image_url": "https://m.media-amazon.com/images/I/51b5V6OQmUL._SX679_.jpg"
        },
        {
            "name": "Bluetooth Speaker",
            "price": 1199,
            "description": "Portable waterproof Bluetooth speaker with deep bass.",
            "brand": "boAt",
            "rating": 4.4,
            "image_url": "https://m.media-amazon.com/images/I/81O0wqUQ9GL._SX679_.jpg"
        },
        {
            "name": "Phone Stand",
            "price": 299,
            "description": "Adjustable metal phone stand for desk use.",
            "brand": "AmazonBasics",
            "rating": 4.1,
            "image_url": "https://m.media-amazon.com/images/I/61wJXrb6v-L._SX679_.jpg"
        },
        {
            "name": "USB Charger",
            "price": 499,
            "description": "Fast-charging USB wall adapter with dual ports.",
            "brand": "Anker",
            "rating": 4.6,
            "image_url": "https://m.media-amazon.com/images/I/61TL0TYM9XL._SX679_.jpg"
        },
        {
            "name": "Laptop Case",
            "price": 799,
            "description": "Water-resistant laptop sleeve with soft inner lining.",
            "brand": "Targus",
            "rating": 4.4,
            "image_url": "https://m.media-amazon.com/images/I/81k+Jgm8hPL._SX679_.jpg"
        },
        {
            "name": "Webcam",
            "price": 1099,
            "description": "HD webcam with microphone and USB plug-n-play.",
            "brand": "Logitech",
            "rating": 4.2,
            "image_url": "https://m.media-amazon.com/images/I/61cWY5Rl+7L._SX679_.jpg"
        },
        {
            "name": "Monitor 24-inch",
            "price": 8999,
            "description": "Full HD LED monitor with HDMI and VGA ports.",
            "brand": "Dell",
            "rating": 4.5,
            "image_url": "https://m.media-amazon.com/images/I/81QpkIctqPL._SX679_.jpg"
        },
        {
            "name": "Power Bank",
            "price": 1499,
            "description": "10,000mAh portable charger with dual output.",
            "brand": "Mi",
            "rating": 4.3,
            "image_url": "https://m.media-amazon.com/images/I/61m+P1aKXzL._SX679_.jpg"
        }
    ]

    for p in fixed_products:
        db.session.add(Product(**p))

    # ✅ Add 100 Fake Products
    faker = Faker()
    for _ in range(100):
        product = Product(
            name=faker.word().capitalize() + " " + faker.word().capitalize(),
            price=random.randint(200, 5000),
            description=faker.sentence(),
            brand=faker.company(),
            rating=round(random.uniform(3.0, 5.0), 1),
            image_url="https://via.placeholder.com/150"
        )
        db.session.add(product)

    db.session.commit()
    return "Database initialized with 110 products"

@app.route("/preview-products")
def preview_products():
    keywords = ["Mouse", "Keyboard", "Lamp", "Speaker", "Stand", "Charger", "Case", "Webcam", "Monitor", "Bank"]

    products = Product.query.filter(
        db.or_(*[Product.name.ilike(f"%{kw}%") for kw in keywords])
    ).all()

    return jsonify([
        {
            "name": p.name,
            "brand": p.brand,
            "price": p.price,
            "rating": p.rating,
            "description": p.description,
            "image_url": p.image_url
        } for p in products
    ])



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
    app.run(port=5002, debug=True)





