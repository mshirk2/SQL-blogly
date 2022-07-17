from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMG = "https://www.nicepng.com/png/detail/128-1280406_view-user-icon-png-user-circle-icon-png.png"


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


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

    tagged = db.relationship('PostTag', backref="posts", cascade="all, delete")

    @property
    def readable_date(self):
        """Return readable datetime"""

        return self.timestamp.strftime("%a %b %-d %Y at %I:%M %p")


class Tag(db.Model):
    """Tag that can be added to posts"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary="post_tags", backref="tags")


class PostTag(db.Model):
    """Tag on a post"""

    __tablename__ = "post_tags"

    post_id = db.Column(
        db.Integer, 
        db.ForeignKey('posts.id'), 
        primary_key=True, 
        nullable=False)
    tag_id = db.Column(
        db.Integer, 
        db.ForeignKey('tags.id'), 
        primary_key=True, 
        nullable=False)

