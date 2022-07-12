from unittest import TestCase
from app import app
from flask import session
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class FlaskTests(TestCase):
    """Tests for user navigation"""

    def setUp(self):
        """Add sample user"""

        User.query.delete()

        user = User(first_name="Testy", last_name="McTestface", image_url="https://cdn.cnn.com/cnnnext/dam/assets/160322031153-london-boat-name-boaty-mcboatface-roth-pkg-00003107-full-169.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction"""
        
        db.session.rollback()

    
