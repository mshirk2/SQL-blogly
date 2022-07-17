from unittest import TestCase
from app import app
from flask import session
from models import db, User, Post, Tag, PostTag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

# Sample profile image URLs
USER_IMG = "https://cdn.cnn.com/cnnnext/dam/assets/160322031153-london-boat-name-boaty-mcboatface-roth-pkg-00003107-full-169.jpg"
USER_IMG2 = "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/close-up-of-cat-wearing-sunglasses-while-sitting-royalty-free-image-1571755145.jpg"



class UserAppTests(TestCase):
    """Tests for user app routes"""

    def setUp(self):
        """Add sample user"""

        user = User(first_name="Testy", last_name="McTestface", image_url=USER_IMG)

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id


    def tearDown(self):
        """Clean up any fouled transaction"""
        
        db.drop_all()
        db.create_all()


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



class PostAppTests(TestCase):
    """Tests for blogpost app routes"""

    def setUp(self):
        """Add sample blogpost"""
        
        user = User(first_name="Testy", last_name="McTestface", image_url=USER_IMG)

        db.session.add(user)
        db.session.commit()

        post = Post(title="Fabulous Test Title", content="Fabulous Test Content", author=user.id)

        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id


    def tearDown(self):
        """Clean up any fouled transaction"""
        
        db.drop_all()
        db.create_all()


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



class TagAppTests(TestCase):
    """Tests for tag app routes"""

    def setUp(self):
        """Add sample tag"""

        tag = Tag(name="test tag")

        db.session.add(tag)
        db.session.commit()

        self.tag_id = tag.id


    def tearDown(self):
        """Clean up any fouled transaction"""
        
        db.drop_all()
        db.create_all()   


    def test_tag_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test tag', html)


    def test_add_tag(self):
        with app.test_client() as client:
            d = {"name": "testingtagthesecond"}
            resp = client.post(f"/tags/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testingtagthesecond", html)


    def test_delete_tag(self):
        with app.test_client() as client:
            resp = client.post(f"tags/{self.tag_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("test tag", html)     
