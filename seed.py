# Seed file for sample data

from models import db, User, Post, Tag, PostTag
from app import app


# Drop all tables, and create them
db.drop_all()
db.create_all()


# Empty tables, just in case
User.query.delete()
Post.query.delete()
Tag.query.delete()


# Sample user image URLs
u1_img = "https://i.insider.com/61d1c0e2aa741500193b2d18?width=1136&format=jpeg"
u2_img = "https://static.standard.co.uk/2021/06/07/12/erik-jan-leusink-IbPxGLgJiMI-unsplash.jpg?width=968&auto=webp&quality=50&crop=968%3A645%2Csmart"
u3_img = "https://discovery.sndimg.com/content/dam/images/discovery/fullset/2021/9/16/GettyImages-1290818736.jpg.rend.hgtvcom.616.411.suffix/1631814091759.jpeg"
u4_img = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjt9-JOz-lORu9dEOsDKBnNATXV4v52keS3Q&usqp=CAU"
u5_img = "https://d3544la1u8djza.cloudfront.net/APHI/Blog/2020/07-23/How+Much+Does+It+Cost+to+Have+a+Cat+_+ASPCA+Pet+Insurance+_+black+cat+with+yellow+eyes+peeking+out-min.jpg"


# Sample users
u1 = User(first_name="Rey", last_name="McSriff", image_url=u1_img)
u2 = User(first_name="Onson", last_name="Sweemey", image_url=u2_img)
u3 = User(first_name="Smeve", last_name="McBichael", image_url=u3_img)
u4 = User(first_name="Todd", last_name="Bonzalez", image_url=u4_img)
u5 = User(first_name="Bobson", last_name="Dugnutt", image_url=u5_img)

db.session.add_all([u1, u2, u3, u4, u5])
db.session.commit()


# Sample posts
p1 = Post(title="Top 10 Cat Food Flavors", content="Meow mwe wow moew meow mwe wow moew meow mwe wow moew meow mwe wow moew meow.", author=3)
p2 = Post(title="How to Destroy a Couch", content="Meeeeeeeeeeeeeeeeeeeeeeeoooooooooooooooooooooooowwwwwwwwwwwwwwwwwww.", author=1)
p3 = Post(title="Grooming Techniques that Don't Quit!", content="Puuurrrghhhhhhhpuuuurrrrghghhhhppppuuuuurrrrrghggghhhh.", author=3)
p4 = Post(title="3 Tips Your Vet Doesn't Want You to Know", content="Puuurrrghhhhhhhpuuuurrrrghghhhhppppuuuuurrrrrghggghhhh.", author=3)
p5 = Post(title="Best Morning Stretches", content="Chirrrrrrrup! Chirrrrrrrrp Chirrrruuuup", author=5)
p6 = Post(title="I Swatted an Entire Charcuterie Platter. Here's how.", content="*stares intently*", author=4)

# Sample tags
t1 = Tag(name="food")
t2 = Tag(name="grooming")
t3 = Tag(name="lifestyle")

db.session.add_all([p1, p2, p3, p4, p5, p6, t1, t2, t3])
db.session.commit()

# Append tags to posts
p1.tagged.append(PostTag(post_id=1, tag_id=1))
p2.tagged.append(PostTag(post_id=2, tag_id=3))
p3.tagged.append(PostTag(post_id=3, tag_id=2))
p4.tagged.append(PostTag(post_id=4, tag_id=1))
p4.tagged.append(PostTag(post_id=4, tag_id=2))
p4.tagged.append(PostTag(post_id=4, tag_id=3))
p5.tagged.append(PostTag(post_id=5, tag_id=3))
p6.tagged.append(PostTag(post_id=6, tag_id=1))
p6.tagged.append(PostTag(post_id=6, tag_id=3))

db.session.add_all([p1, p2, p3, p4, p5, p6])
db.session.commit()