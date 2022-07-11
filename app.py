"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

@app.route("/")
def homepage():
    """List users"""

    users = User.query.all()
    return render_template("index.html", users=users)


@app.route("/add-user", methods=["POST"])
def add_user():
    """Handle form submit, redirect to new user detail page"""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect (f"/{user.id}")

@app.route("/create")
def create_user():
    """Render new user form"""

    return render_template("create.html")

@app.route("/<int:user_id>")
def user_detail(user_id):
    """Show user details"""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

@app.route("/<int:user_id>/edit")
def edit_user():
    """Edit user"""

    return render_template("edit.html")

