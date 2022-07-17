"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Debug Toolbar
from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)


@app.route("/")
def homepage():
    """Home page with recent posts"""

    posts = Post.query.order_by(Post.timestamp.desc()).limit(5).all()
    return render_template("homepage.html", posts=posts)



############ User Routes

@app.route("/users")
def show_users():
    """Show all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users/index.html", users=users)


@app.route("/users/new", methods=["GET"])
def new_user_form():
    """Render new user form"""

    return render_template("users/new-user.html")

  
@app.route("/users/new", methods=["POST"])
def new_user_submit():
    """Handle new user form submit, redirect to users list"""

    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect ("/users")


@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show user details"""

    user = User.query.get_or_404(user_id)
    return render_template("users/detail.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    """Render edit user form """

    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_submit(user_id):
    """Handle edit user form submit, redirect to users list"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect ("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")




############ Blog Post Routes

@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def new_post(user_id):
    """Render new post form"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("/users/new-post.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post_submit(user_id):
    """Handle new post submit, redirect to user detail page"""

    user = User.query.get_or_404(user_id)
    new_post = Post(
            title = request.form['title'],
            content = request.form['content'],
            author = user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect (f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show post, with buttons to edit or delete post"""

    post = Post.query.get_or_404(post_id)
    return render_template("posts/detail.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Render edit post form """

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("posts/edit.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post_submit(post_id):
    """Handle edit post form submit, redirect to post detail"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect (f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect("/users")


############ Tag Routes

@app.route("/tags")
def show_tags():
    """Lists all tags, with links to the tag detail page."""

    tags = Tag.query.order_by(Tag.name).all()
    return render_template("tags/index.html", tags=tags)


@app.route("/tags/new", methods=["GET"])
def new_tag_form():
    """Render new tag form"""

    posts = Post.query.all()
    return render_template("tags/new.html", posts=posts)


@app.route("/tags/new", methods=["POST"])
def new_tag_submit():
    """Handle new tag form submit, redirect to tag list"""

    new_tag = Tag(name = request.form['name'])
    post_ids = [int(num) for num in request.form.getlist("posts")]
    new_tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(new_tag)
    db.session.commit()

    return redirect ("/tags")


@app.route("/tags/<int:tag_id>")
def tag_detail(tag_id):
    """Show detail about a tag, with links to edit form and to delete."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template("tags/detail.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """Render edit tag form """

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template("tags/edit.html", tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag_submit(tag_id):
    """Handle edit tag form submit, redirect to tag list"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect (f"/tags/{tag.id}")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")