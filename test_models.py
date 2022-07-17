from unittest import TestCase
from app import app
from models import db, User, Post, Tag, PostTag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserModelTest(TestCase):
    """Tests for User Model"""

    def setUp(self):
        """Clean up any existing users"""
        User.query.delete()


    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()


    def test_full_name(self):
        """Tests that the full_name method returns first and last name"""

        user = User(first_name="Testy", last_name="McTestface", image_url="https://cdn.cnn.com/cnnnext/dam/assets/160322031153-london-boat-name-boaty-mcboatface-roth-pkg-00003107-full-169.jpg")

        self.assertEqual(user.full_name, 'Testy McTestface')