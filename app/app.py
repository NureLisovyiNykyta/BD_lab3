from app.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.routes import sales_bp, goods_bp, departments_bp
    app.register_blueprint(sales_bp)
    app.register_blueprint(goods_bp)
    app.register_blueprint(departments_bp)

    return app
