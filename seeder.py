from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Item, User

import datetime

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

now = datetime.datetime.now()

# users
user1 = User(name = "Nouf", email = "nalturaief@yahoo.com", picture = "https://content-static.upwork.com/uploads/2014/10/01073427/profilephoto1.jpg")
session.add(user1)
session.commit()

user2 = User(name = "Sara", email = "sara@gmail.com", picture = "https://i.pinimg.com/originals/52/61/13/52611340f103ae8c2521b5213919c21d.jpg")
session.add(user1)
session.commit()

#items for Necklaces category
category1 = Category(name = "Necklaces", picture = "https://images.unsplash.com/photo-1511253819057-5408d4d70465?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80")
session.add(category1)
session.commit()

item1 = Item(name = "Infinity", description = "Infinity is a powerful symbol of continuous connection, energy and vitality. The simple and striking infinity symbol adds a modern touch to this necklace.", dateAdded = now.isoformat(), category = category1, user = user1)
session.add(item1)
session.commit()

item2 = Item(name = "Key Stem", description = "Feminine and delicate, the designs of the Fleur de Lis collection offer a refined sense of graceful empowerment that speaks to quiet confidence. This simple design shines with dazzling diamonds.", dateAdded = now.isoformat(), category = category1, user = user2)
session.add(item2)
session.commit()


#items for Rings category
category1 = Category(name = "Rings", picture = "https://images.unsplash.com/photo-1512163143273-bde0e3cc7407?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80")
session.add(category1)
session.commit()

item1 = Item(name = "Diamond Open Flower ", description = "Inspired by the idea of abstract flower petals, the new Paper Flowers collection is a balance of refined femininity and industrial modernity.", dateAdded = now.isoformat(), category = category1, user = user2)
session.add(item1)
session.commit()

item2 = Item(name = "True Diamond Link", description = "Graphic angles and clean lines blend to create the beautiful clarity of the T collection. This link ring reimagines an iconic T motif to reveal a striking center diamond.", dateAdded = now.isoformat(), category = category1, user = user1)
session.add(item2)
session.commit()

#items for Earings category
category1 = Category(name = "Earings", picture = "https://i.imgur.com/WD7qcpb.jpg")
session.add(category1)
session.commit()

item1 = Item(name = "Blue Diamond", description = "Earrings in platinum with diamonds and aquamarines.", dateAdded = now.isoformat(), category = category1, user = user2)
session.add(item1)
session.commit()

print "added catalog items!"
