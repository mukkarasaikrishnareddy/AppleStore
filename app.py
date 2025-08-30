from flask import Flask
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_secret_key"
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(product_bp, url_prefix="/api/products")
app.register_blueprint(cart_bp, url_prefix="/api/cart")

@app.route("/")
def home():
    return {"message": "Apple Store API is running!"}

from routes.payment_routes import payment_bp

app.register_blueprint(payment_bp, url_prefix="/api/payment")


if __name__ == "__main__":
    app.run(debug=True)
