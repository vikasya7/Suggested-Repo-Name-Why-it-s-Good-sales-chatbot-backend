from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
import random
from sqlalchemy import or_


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


def init_db():
    db.drop_all()
    db.create_all()

    # ✅ 10 Real Products with static Unsplash image URLs
    fixed_products = [
        {
            "name": "Wireless Mouse",
            "price": 499,
            "description": "Ergonomic wireless mouse with smooth tracking and USB receiver.",
            "brand": "Logitech",
            "rating": 4.5,
            "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3"
        },
        {
            "name": "Gaming Keyboard",
            "price": 1499,
            "description": "Mechanical RGB keyboard with blue switches and metal frame.",
            "brand": "Redragon",
            "rating": 4.7,
            "image_url": "https://images.unsplash.com/photo-1610465299993-ff978956b6b6"
        },
        {
            "name": "LED Desk Lamp",
            "price": 899,
            "description": "Foldable LED lamp with USB charging and adjustable brightness.",
            "brand": "Philips",
            "rating": 4.3,
            "image_url": "https://images.unsplash.com/photo-1512295767273-ac109ac3acfa"
        },
        {
            "name": "Bluetooth Speaker",
            "price": 1199,
            "description": "Portable waterproof Bluetooth speaker with deep bass.",
            "brand": "boAt",
            "rating": 4.4,
            "image_url": "https://images.unsplash.com/photo-1593809787529-19d0f7d2b873"
        },
        {
            "name": "Phone Stand",
            "price": 299,
            "description": "Adjustable metal phone stand for desk use.",
            "brand": "AmazonBasics",
            "rating": 4.1,
            "image_url": "https://images.unsplash.com/photo-1611078481462-1e4b8fcfd7c3"
        },
        {
            "name": "USB Charger",
            "price": 499,
            "description": "Fast-charging USB wall adapter with dual ports.",
            "brand": "Anker",
            "rating": 4.6,
            "image_url": "https://images.unsplash.com/photo-1580910051070-49e3ff7c7e4d"
        },
        {
            "name": "Laptop Case",
            "price": 799,
            "description": "Water-resistant laptop sleeve with soft inner lining.",
            "brand": "Targus",
            "rating": 4.4,
            "image_url": "https://images.unsplash.com/photo-1603791452906-5d2c799dc322"
        },
        {
            "name": "Webcam",
            "price": 1099,
            "description": "HD webcam with microphone and USB plug-n-play.",
            "brand": "Logitech",
            "rating": 4.2,
            "image_url": "https://images.unsplash.com/photo-1596558450263-c0a4f6b6cdcc"
        },
        {
            "name": "Monitor 24-inch",
            "price": 8999,
            "description": "Full HD LED monitor with HDMI and VGA ports.",
            "brand": "Dell",
            "rating": 4.5,
            "image_url": "https://images.unsplash.com/photo-1587825140708-dfaf72f22c4e"
        },
        {
            "name": "Power Bank",
            "price": 1499,
            "description": "10,000mAh portable charger with dual output.",
            "brand": "Mi",
            "rating": 4.3,
            "image_url": "https://images.unsplash.com/photo-1599691754830-c0ed8f6d7e27"
        }
    ]

    for p in fixed_products:
        db.session.add(Product(**p))

    # ✅ 100 Faker Products with Picsum placeholder images
    faker = Faker()
    for _ in range(100):
        product = Product(
            name=faker.word().capitalize() + " " + faker.word().capitalize(),
            price=random.randint(200, 5000),
            description=faker.sentence(),
            brand=faker.company(),
            rating=round(random.uniform(3.0, 5.0), 1),
            image_url=f"https://picsum.photos/200/150?random={random.randint(1, 1000)}"
        )
        db.session.add(product)

    db.session.commit()
    return "✅ Database initialized with 110 products (10 real + 100 fake)"




@app.route("/preview-products")
def preview_products():
    keywords = ["Mouse", "Keyboard", "Lamp", "Speaker", "Stand", "Charger", "Case", "Webcam", "Monitor", "Bank"]

    products = Product.query.filter(
        or_(*[Product.name.ilike(f"%{kw}%") for kw in keywords])
    ).all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "brand": p.brand,
            "rating": p.rating,
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



@app.route('/chatbot-query', methods=["POST"])
def chatbot_query():
    data = request.get_json()
    query = data.get("query", "").lower()

    matches = Product.query.filter(Product.name.ilike(f"%{query}%")).all()

    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,  
            "brand": p.brand,              
            "rating": p.rating,
            "image_url": p.image_url       
        } for p in matches
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
    app.run(port=5003, debug=True)





