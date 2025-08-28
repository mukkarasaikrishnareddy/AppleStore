from flask import Flask
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(product_bp, url_prefix="/api/products")
app.register_blueprint(cart_bp, url_prefix="/api/cart")

@app.route("/")
def home():
    return {"message": "Apple Store API is running!"}

if __name__ == "__main__":
    app.run(debug=True)
