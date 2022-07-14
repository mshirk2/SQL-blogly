from unittest import TestCase
from app import app
from flask import session
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

# Some sample profile image URLs
USER_IMG = "https://cdn.cnn.com/cnnnext/dam/assets/160322031153-london-boat-name-boaty-mcboatface-roth-pkg-00003107-full-169.jpg"
USER_IMG2 = "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/close-up-of-cat-wearing-sunglasses-while-sitting-royalty-free-image-1571755145.jpg"


class FlaskTests(TestCase):
    """Tests for user navigation"""

    def setUp(self):
        """Add testing data"""

        # User.query.delete()
        # Post.query.delete()

        ########### Set up user

        user = User(
            first_name="Testy", 
            last_name="McTestface", 
            image_url=USER_IMG)

        db.session.add(user)
        db.session.commit()


        ########### Set up post
        post = Post(
            title="Fabulous Test Title", 
            content="Fabulous Test Content", 
            author=user.id)
        
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id


    def tearDown(self):
        """Clean up any fouled transaction"""
        
        db.session.rollback()

    ######################### User tests

    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Testy', html)
    

    def test_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Testy McTestface', html)


    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Testy2", "last_name": "McTestface2", "image_url": USER_IMG2}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Testy2", html)


    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name": "Testy3", "last_name": "McTestface3", "image_url": USER_IMG2}
            resp = client.post("/users/1/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Testy3", html)


    ####################### Post tests

    def test_post_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Fabulous Test Title', html)


    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "Title2", "content": "Another wonderful post", "author": f"{self.user_id}"}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Title2", html)


    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post("posts/1/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Fabulous Test Title", html)


    
