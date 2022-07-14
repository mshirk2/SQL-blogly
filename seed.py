from app import app
from models import db, User, Post


# Drop all tables, and create them
db.drop_all()
db.create_all()


# Empty tables, just in case
User.query.delete()
Post.query.delete()


# Seed user image URLs
u1_img = "https://i.insider.com/61d1c0e2aa741500193b2d18?width=1136&format=jpeg"
u2_img = "https://i.pinimg.com/originals/bb/af/a5/bbafa5688a7e64c4431a3b575f9035c6.jpg"
u3_img = "https://discovery.sndimg.com/content/dam/images/discovery/fullset/2021/9/16/GettyImages-1290818736.jpg.rend.hgtvcom.616.411.suffix/1631814091759.jpeg"


# Sample users
u1 = User(first_name="Rey", last_name="McSriff", image_url=u1_img)
u2 = User(first_name="Onson", last_name="Sweemey", image_url=u2_img)
u3 = User(first_name="Smeve", last_name="McBichael", image_url=u3_img)


db.session.add_all([u1, u2, u3])
db.session.commit()


p1 = Post(title="Top 10 Cat Food Flavors", content="Meow mwe wow moew meow mwe wow moew meow mwe wow moew meow mwe wow moew meow.", author=3)
p2 = Post(title="How to Destroy a Couch", content="Meeeeeeeeeeeeeeeeeeeeeeeoooooooooooooooooooooooowwwwwwwwwwwwwwwwwww.", author=1)
p3 = Post(title="Grooming Techniques that Don't Quit!", content="Puuurrrghhhhhhhpuuuurrrrghghhhhppppuuuuurrrrrghggghhhh.", author=3)


db.session.add_all([p1, p2, p3])
db.session.commit()