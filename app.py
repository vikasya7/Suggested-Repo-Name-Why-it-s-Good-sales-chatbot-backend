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

# Models
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

# Routes
@app.route('/')
def index():
    return "✅ Backend API is running"

# @app.route("/init-db")
# def init_db():
#     db.drop_all()
#     db.create_all()

#     # ✅ 10 Real Products with Imgur image URLs (No Unsplash / No CORS Issue)
#     fixed_products = [
#         {
#             "name": "Wireless Mouse",
#             "price": 499,
#             "description": "Ergonomic wireless mouse with smooth tracking and USB receiver.",
#             "brand": "Logitech",
#             "rating": 4.5,
#             "image_url": "https://www.shutterstock.com/image-photo/wireless-computer-mouse-isolated-on-260nw-95568295.jpg"
#         },
#         {
#             "name": "Gaming Keyboard",
#             "price": 1499,
#             "description": "Mechanical RGB keyboard with blue switches and metal frame.",
#             "brand": "Redragon",
#             "rating": 4.7,
#             "image_url": "https://www.shutterstock.com/image-photo/stylish-gaming-mouse-keyboard-rainbow-260nw-1956033031.jpg"
#         },
#         {
#             "name": "LED Desk Lamp",
#             "price": 899,
#             "description": "Foldable LED lamp with USB charging and adjustable brightness.",
#             "brand": "Philips",
#             "rating": 4.3,
#             "image_url": "https://5.imimg.com/data5/SELLER/Default/2021/12/RP/SY/JO/25945379/whatsapp-image-2021-12-10-at-4-40-10-pm-4--500x500.jpeg"
#         },
#         {
#             "name": "Bluetooth Speaker",
#             "price": 1199,
#             "description": "Portable waterproof Bluetooth speaker with deep bass.",
#             "brand": "boAt",
#             "rating": 4.4,
#             "image_url": "https://www.shutterstock.com/image-photo/black-portable-mini-speaker-colorful-600nw-2561079163.jpg"
#         },
#         {
#             "name": "Phone Stand",
#             "price": 299,
#             "description": "Adjustable metal phone stand for desk use.",
#             "brand": "AmazonBasics",
#             "rating": 4.1,
#             "image_url": "https://www.shutterstock.com/image-photo/smartphone-stands-on-wooden-stand-260nw-1788873725.jpg"
#         },
#         {
#             "name": "USB Charger",
#             "price": 499,
#             "description": "Fast-charging USB wall adapter with dual ports.",
#             "brand": "Anker",
#             "rating": 4.6,
#             "image_url": "https://www.shutterstock.com/image-photo/cable-usb-micro-connector-on-260nw-2501127037.jpg"
#         },
#         {
#             "name": "Laptop Case",
#             "price": 799,
#             "description": "Water-resistant laptop sleeve with soft inner lining.",
#             "brand": "Targus",
#             "rating": 4.4,
#             "image_url": "https://safaribags.com/cdn/shop/files/1_5b1b3058-dad7-4b8c-969d-07b1bccb110e.jpg?v=1688114256"
#         },
#         {
#             "name": "Webcam",
#             "price": 1099,
#             "description": "HD webcam with microphone and USB plug-n-play.",
#             "brand": "Logitech",
#             "rating": 4.2,
#             "image_url": "https://images.unsplash.com/photo-1623949556303-b0d17d198863?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8d2ViY2FtfGVufDB8fDB8fHww"
#         },
#         {
#             "name": "Monitor 24-inch",
#             "price": 8999,
#             "description": "Full HD LED monitor with HDMI and VGA ports.",
#             "brand": "Dell",
#             "rating": 4.5,
#             "image_url": "https://cdn.thewirecutter.com/wp-content/media/2024/09/27inchmonitor-2048px-DSF4695.jpg"
#         },
#         {
#             "name": "Power Bank",
#             "price": 1499,
#             "description": "10,000mAh portable charger with dual output.",
#             "brand": "Mi",
#             "rating": 4.3,
#             "image_url": "https://media-ik.croma.com/prod/https://media.croma.com/image/upload/v1725624590/275990_0_nj9tzm.png"
#         }
#     ]

#     for p in fixed_products:
#         db.session.add(Product(**p))

#     # ✅ Faker Products (100 dummy ones)
#     for _ in range(100):
#         product = Product(
#             name=faker.word().capitalize() + " " + faker.word().capitalize(),
#             price=random.randint(200, 5000),
#             description=faker.sentence(),
#             brand=faker.company(),
#             rating=round(random.uniform(3.0, 5.0), 1),
#             image_url=f"https://picsum.photos/200/150?random={random.randint(1, 1000)}"
#         )
#         db.session.add(product)

#     db.session.commit()
#     return "✅ Database initialized with 110 products (10 real with images + 100 fake)"

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

@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({"message": "Login successful"})
    return jsonify({"error": "Invalid credentials"}), 401

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

@app.route("/track-order", methods=["POST"])
def track_order():
    data = request.get_json()
    order_id = data.get("order_id", "")

    # Dummy status list for now
    statuses = ["Processing", "Shipped", "Out for delivery", "Delivered"]

    if order_id:
        status = random.choice(statuses)
        return jsonify({"order_id": order_id, "status": status})
    else:
        return jsonify({"error": "Order ID is missing."}), 400




if __name__ == "__main__":
    app.run(port=5003, debug=True)












