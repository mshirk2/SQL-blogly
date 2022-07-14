from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMG = "https://www.nicepng.com/png/detail/128-1280406_view-user-icon-png-user-circle-icon-png.png"


class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, default=DEFAULT_IMG)   

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return user's full name"""

        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        u = self
        return f"User {u.id} {u.first_name} {u.last_name}"


class Post(db.Model):
    """Blog Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(
        db.DateTime, 
        nullable=False, 
        default=datetime.datetime.now)
    author = db.Column(
        db.Integer, 
        db.ForeignKey('users.id'), 
        nullable=False)

    @property
    def readable_date(self):
        """Return readable datetime"""

        return self.timestamp.strftime("%a %b %-d %Y at %I:%M %p")



def seed_data():
    """Starter data"""

    db.drop_all()
    db.create_all()

    User.query.delete()
    Post.query.delete()

    # Seed user image URLs
    u1_img = "https://i.insider.com/61d1c0e2aa741500193b2d18?width=1136&format=jpeg"
    u2_img = "https://i.pinimg.com/originals/bb/af/a5/bbafa5688a7e64c4431a3b575f9035c6.jpg"
    u3_img = "https://discovery.sndimg.com/content/dam/images/discovery/fullset/2021/9/16/GettyImages-1290818736.jpg.rend.hgtvcom.616.411.suffix/1631814091759.jpeg"

    # Sample users
    u1 = User(first_name="Rey", last_name="McSriff", image_url=u1_img)
    u2 = User(first_name="Onson", last_name="Sweemey", image_url=u2_img)
    u3 = User(first_name="Sleve", last_name="McDichael", image_url=u3_img)

    db.session.add_all([u1, u2, u3])
    db.session.commit()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    seed_data()
