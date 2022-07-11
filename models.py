from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(), nullable=False, default="https://www.nicepng.com/png/detail/128-1280406_view-user-icon-png-user-circle-icon-png.png")   
