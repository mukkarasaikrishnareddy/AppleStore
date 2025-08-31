import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Import blueprints
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.cart_routes import cart_bp
from routes.order_routes import order_bp
from routes.payment_routes import payment_bp

# Import custom JSON encoder (for Mongo ObjectId serialization)
from utils.json_encoder import JSONEncoder


def create_app():
    app = Flask(__name__)

    # 🔑 Handle ObjectId -> str globally
    app.json_encoder = JSONEncoder

    # JWT config
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret")
    JWTManager(app)

    # Enable CORS
    CORS(app)
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    app.register_blueprint(order_bp, url_prefix="/api/orders")
    app.register_blueprint(payment_bp, url_prefix="/api/payment")

    # Health check route
    @app.route("/")
    def home():
        return {"message": "🍎 Apple Store API is running successfully!"}

    # Optional favicon handler (avoid 404 in browser)
    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon"
        )

    return app
if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"

    app = create_app()
    app.run(host=host, port=port, debug=debug)
